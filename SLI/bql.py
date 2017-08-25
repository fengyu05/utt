#!/usr/bin/python
import sys, os, time
import urllib
import json
import subprocess
import urllib

options ={}
args = []

# comments are tables names for reference purpose
HOST = {
    'adsClick' : 'adsClickPinotStatistics', #adsClickEvents
    'adAnalyticsEvent' :   'adAnalyticsEventsPinotStatistics', #adAnalyticsEvent
    'audienceCount':  'audienceCountPinotStatistics', #audienceCount
    'adsAnalytics' : 'adsAnalyticsPinotStatistics', #adsAnalytics
    'scinAds' : 'adsAnalyticsPinotStatistics',
    'bids' : 'bidSuggestPinotStatistics', #bidSuggestion
    'conversionTracking' :  'conversionTrackingPinotStatistics', #conversionTrackingStatistics
    'scin': 'scinForecastingPinotStatistics', #scinForecasting
    'inmail': 'scinInmailForecastingPinotStatistics', #scinInmailForecasting
    'adsReport': 'adsReportingPinotStatistics',
    'scinClick': 'adsAnalyticsPinotStatistics',
    'scinPricing':  'scinPricingPinotStatistics', #scinPricing
    'ssuPricing': 'ssuPricingPinotStatistics',  #ssuPricingEvents
    'native' :  'nativeAdsForecastPinotStatistics', #nativeAdsForecasting
    'pacing'  : 'liAdsPacingPinotStatistics', #liAdsPacing
    'inmailAnalytics' : 'sponsoredInMailAnalyticsPinotStatistics', #sponsoredInMailAnalytics
<<<<<<< HEAD
=======
    'forecast' : 'jobForecastingPinotStatistics',
>>>>>>> a72cff051cc200fcb8997f285af5be7aac2f585d
    'job' : 'jobForecastingPinotStatistics',
}

TEE_TMP = '/tmp/tee.bql'
CURLI = '/usr/local/linkedin/bin/curli'

def teeRun(cmd):
  cmd = cmd + ' | tee %s' % TEE_TMP
  pipeRun(cmd)
  result = open(TEE_TMP).read()

  return result

def envRun(cmd):
  env = options.env
  cmd = cmd
  if env.startswith('prod-'):
    cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  return teeRun(cmd)

def pipeRun(cmd):
  print cmd
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            shell=True)
  output, error = p.communicate()

  if not options.resultOnly:
    print output
    print error
  return output


def makeFabric():
  if options.env:
    return '--fabric=%s' % options.env
  else:
    return ''

def getPinotHost(host):
  if host in HOST:
    return HOST[host]
  else:
    return host

def bql(host, query):
  host = getPinotHost(host)
  url = 'd2://%s?q=statistics&bqlRequest=%s' % (host, urllib.quote(query))

  curliCmd = CURLI + ' --pretty-print %s \'%s\' -X GET -g' % (makeFabric(), url)
  result = envRun(curliCmd)
  if options.resultOnly:
    result = filterRestResult(result)
    result = getResult(result)
  print result

def getResult(jobsResult):
  return float(str(jobsResult[u'elements'][0][u'results'][0][0]))

def filterRestResult(result):
  lines = result.split('\n')

  started = False
  if options.env.find('prod') == -1:
    started = True
  jsonLines = []
  for line in lines:
    if options.env.find('prod') != -1 and line.count('{') > 0:
      started = True
    if started:
      jsonLines.append(line)
  resultJson = json.loads(''.join(jsonLines))
  return resultJson

def printHelp():
  print """
  bql.py host query  [--env=prod-lva1]
  """

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='ei-lca1', help='env')
  parser.add_option('-r', '--resultOnly', dest='resultOnly', action='store_true', help='return result only')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if len(args) < 1:
    printHelp()
    exit(1)

  bql(*args)

