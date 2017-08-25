#!/usr/bin/python
import sys, os, time

import re

RESOURCES = {
  'creative': 'adCreatives',
  'campaign': 'adCampaigns',
  'account': 'adAccounts',
  'advertiser': 'adAccounts',
}



BASE_CMD = 'curli %s --pretty-print \'d2://%s/%s\''
GET_CMD = ' -X GET'
POST_METHOD_CMD = ' -X POST -H \'X-RestLi-Method: %s\''
SEARCH_CMD = 'curli %s --pretty-print \'d2://%s?q=search'

AUTH_HEADER = ' -H \'Authenticate: X-RestLi SUPERUSER:urn:li:system:0\''

KEY_REPLACES = {
'ID': '111541749',
'MS_ID_TEST':'502269511',
'MS_ID_LIVE':'502215307',
'TEST_AD': '99246671',
'TEST_AD2' : '99252021',
'SU_LIVE': '32469513',
}

def envRun(env, cmd):
  cmd = cmd
  if env.startswith('prod-'):
    cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  printRun(cmd)

def printRun(cmd):
  print cmd
  os.system(cmd)

def quoteValue(v):
  if v == 'false' or v == 'ture' or v == 'null':
    return v
  elif type(v) == int or type(v) == float:
    return v
  else:
    return '"' + v + '"'

def makeFieldsFromDict(dict):
  dictContent = ''
  for k, v in dict.iteritems():
    if k.find(':') != -1:
      subKs = k.split(':')

      content = ''
      index = 0
      for subK in subKs:
        index += 1
        if index == len(subKs):
          content += '"%s" :' % subK
        else:
          content += '"%s" : { ' % subK

      content += quoteValue(v)
      content += '}' * (len(subKs) + 1)
      content += ','

      dictContent += content
    else:
      dictContent += '"%s" : %s,' %(k, quoteValue(v))

  dictContent = dictContent[:-1]
  return dictContent

def makePatchSessionFromDict(dict):
  result = ' --data \'{ "patch": {"$set":{ %s }}}\''

  dictContent = makeFieldsFromDict(dict)

  return result % dictContent

def makeFarbicArg():
  if options.env:
    return '--fabric %s' % options.env
  else:
    return ''

def getAction(id):

  cmd = BASE_CMD % (makeFarbicArg(), options.resource, id) + GET_CMD
  envRun(options.env, cmd)

def makeAuthHeader():
  return AUTH_HEADER

def partialUpdate(id, patch):
  cmd = BASE_CMD % (makeAuthHeader(), options.resource, id) + POST_METHOD_CMD % 'partial_update'

  data = {}
  fields = patch.split(',')
  for field in fields:
    pair = field.split('=')
    key = pair[0].strip()
    value = ""
    try:
      value = int(pair[1].strip())
    except:
      value = pair[1].strip()

    print 'Patch item:', key, value
    data[key] = value

  cmd = cmd + makePatchSessionFromDict(data) + makeAuthHeader()

  envRun(options.env, cmd)

def rawPatchUpdate(id, patch):
  cmd = BASE_CMD % (makeAuthHeader(), options.resource, id) + POST_METHOD_CMD % 'partial_update'

  cmd = cmd +  ' --data \'{ "patch": {"$set":{ %s }}}\'' % patch + makeAuthHeader()

  envRun(options.env, cmd)

def makeFacet(facet):
  facetFileds = facet.split(',')
  result = ''
  for i in xrange(len(facetFileds) / 2):
    keyIdx = i * 2
    valueIdx = i * 2 + 1
    result += '&facet=%s,%s' % (facetFileds[keyIdx], facetFileds[valueIdx])

  return result


def search(facet):
  facet = makeFacet(facet)
  cmd = SEARCH_CMD % (makeFarbicArg(), options.resource)
  cmd = cmd + facet + "'" + GET_CMD
  envRun(options.env, cmd)


def create(fields):
  print fields

def newCreative():
  pass

def main():
  ALL_ACTION = {
      'get': getAction,
      'partial': partialUpdate,
      'search': search,
      'patch': rawPatchUpdate,
      'create': create,
  }
  GLOBALS_CMD = {
      'newCreative': newCreative,
  }

  if args[0] in RESOURCES:
    setattr(options, 'resource', RESOURCES[args[0]])
    action = args[1]
    ALL_ACTION[action](*args[2:])
    return
  elif args[0] in GLOBALS_CMD:
    cmd = args[0]
    GLOBALS_CMD[cmd](*args[1:])
  else:
    print 'action %s not found' % action
    printHelp()
    exit(1)

  print ('\n\n')

def printHelp():
  print 'sasRest.py campaign|creative|account... [args]'
  print 'sasRest.py creative [args]'
  return 0

def replaceArgs(args):
  for k, v in KEY_REPLACES.iteritems():
    args = [ re.sub(r"\b%s\b" % k, v, x) for x in args]
  return args

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='', help='env')

  (options,args) = parser.parse_args()
  args = replaceArgs(args)

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if (len(args) <= 2):
    parser.print_help()
    printHelp()
    exit()

  main()

