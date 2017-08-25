#!/usr/bin/python
import sys, os, time
import urllib
import json
import subprocess

host = 'd2://adCreatives'
local_host = 'localhost:10038/sas-campaign/resources/adCreatives'

options ={}
args = []

def makeAuthHeader(creatorUrn):
  return ' -H \'Authenticate: X-RestLi %s\'' % creatorUrn

def envRun(cmd):
  env = options.env
  cmd = cmd
  if env.startswith('prod-'):
    cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  return pipeRun(cmd)

def pipeRun(cmd):
  print cmd
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            shell=True)
  output, error = p.communicate()
  print output
  print error

  return output


PRE_CHECK = 'pre'
CUR_CHECK = 'cur'
ALL_CHECK = 'all'


TEST_CAMPIGN_URN = 'urn:li:sponsoredCampaign:320033061'
TEST_CREATOR_URN = 'urn:li:member:16694691'
TEST_PASSWORD = 'password'
UNKOWN_URN = 'urn:li:unknown:0'


def makeDataSection(dataDict):
  result = ' --data \'{'
  for key, value in dataDict.iteritems():
    result += ' \"%s\" : \"%s\" ,' % (key, value)

  result = result[:-1] + '}\''
  return result

def makeCreative(dataDict):
  return ('{ "partitionId" : 16694691 ,  "parent" : "%s", "type" : "TEXT_AD",  "variables": { "href" : "%s", "subType" : ' +\
      '{"com.linkedin.tscp.TextAdCreativeVariables" : { "title" : "%s", "text" : "%s"} }} }') %\
      (dataDict["campaignUrn"], dataDict["creativeUrl"], dataDict["creativeTitle"], dataDict["creativeText"])

def makeCreativeSession(dataDict):
  result = ' --data \'{ \"creative\" : %s }\'' % makeCreative(dataDict)
  return result



def checkCreative(title, text, url, campaignUrn=TEST_CAMPIGN_URN, creatorUrn=TEST_CREATOR_URN, creatorPass=TEST_PASSWORD):

  if options.historical:
    resource = '%s?action=validateCreativeQuality' % host
  else:
    resource = '%s?action=validateCreative' % host

  dataDict = {
      "creativeTitle": title,
      "creativeText": text,
      "creativeUrl": url,
      "campaignUrn": campaignUrn,
      "creatorUrn": creatorUrn
  }

  curliCmd = 'curli %s --pretty-print "%s" -X POST -H X-RestLi-Method:action --user %s --password %s' % (makeAuthHeader(creatorUrn), resource, creatorUrn, creatorPass) + makeCreativeSession(dataDict)
  return envRun(curliCmd)


def assertError(result, expectedErrors):
  result = json.loads(result)

  if options.historical:
    errors = [ str(x) for x in sorted(result[u'value'][u'validationErrors'])]
  else:
    errors = [ str(x[u'errorType']) for x in (result[u'value'][u'validationErrors'])]
    errors = sorted(errors)
  assert expectedErrors == errors

def allCheck():
  ################################ NEGATIVE TESTS
  result = checkCreative('test ad jfkldsjaflkdjsalkfjjfkldsa', 'jfkdlsajfkd', 'g.cn');
  assertError(result, ['TEST_LOOKLIKE_ADS'])

  result = checkCreative('este es un anuncio', 'vendemos libro vendemos libro vendemos libro, vendemos libro vendemos libro vendemos libro, vendemos libro vendemos libro vendemos libro', 'g.cn');
  assertError(result, ['CREATIVE_LANGUAGE_MISMATCH'])

  result = checkCreative('Datam architets', 'Have you haead of the fuid duata layer? ', 'g.cn');
  assertError(result, ['MISSPELLED_WORDS', 'TEST_LOOKLIKE_ADS'])

  result = checkCreative('>>> Data architets <<<', 'Have you head of the fluid data layer? ', 'g.cn');
  assertError(result, ['INAPPROPRIATE_PUNCTUATION'])

  result = checkCreative('Data architcets of LinkedIN', 'Have you head of the fluid data layer? ', 'g.cn');
  assertError(result, ['MENTIONED_LINKEDIN'])

  result = checkCreative('DATA architcets', 'HAVE YOU HEAD of the fluid data layer? ', 'g.cn');
  assertError(result, ['TOO_MANY_CAPS'])

  result = checkCreative('fuck', 'fuck', '');
  assertError(result, ['INAPPROPRIATE_CONTENT'])

  # test empty ref
  result = checkCreative('data', 'have you head of the fluid data layer?', '');
  assertError(result, [])

  result = checkCreative('', '', '');
  assertError(result, [])
  ######################### POSITIVE TESTS

def printHelp():
  print """
  validateCreative.py [--env=prod-lva1]
  """

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='', help='env')
  parser.add_option('--historical', action='store_true', help='historical api')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if len(args) == 0:
    allCheck()
    exit(0)

  ALL_ACTION = {
            CUR_CHECK: checkCreative,
            ALL_CHECK: allCheck,
  }

  action = args[0]

  if action not in ALL_ACTION:
    print 'action %s not found' % action
    printHelp()
    exit(1)

  ALL_ACTION[action](*args[1:])

