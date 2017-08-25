#!/usr/bin/python
import sys, os, time
import urllib
import json
import subprocess
import urllib

options = {}
args = []

QUERIES = [
  ['geos:na.us'],
  ['geos:as.cn'],
  ['geos:na.us','gender:m'],
  ['geos:na.us','yearsOfExperience:5-7'],
  ['geos:na.us,as.zh','gender:m','yearsOfExperience:5-7']
]

HOST = 'd2://adForecasts'
PROTOCOL = 'http'
PORT = '2553'
PATH = '/tscp-forecast/resources/adForecasts'
PRODUCT = 'tscp-forecast'

# allow variance below this threshold
EI_DATA_VALIDATION_THRESHOLD = 0.01
PROD_DATA_VALIDATION_THRESHOLD = 0.005

FABRICS = {
  'ei': 'ei-ltx1',
  'prod': 'prod-ltx1'
}

CAMPAIGN_TYPES = [
  'SPONSORED_STATUS_UPDATES_V2',
  'SPONSORED_INMAILS',
  'DYNAMIC'
]

DAYS = 7

FINDER_NAME = 'supplyCriteria'
TOTAL_FINDER_NAME = 'totalSupplyCriteria'
EXTERNAL_FINDER_NAME = 'supplyCriteriaWithTargetSpec'

CMD_CURLI = '/usr/local/linkedin/bin/curli'
CMD_RAIN = '/usr/local/linkedin/bin/rain'

TEE_TMP = '/tmp/tee.fcst'

TSCP_ADMIN_CORE = {}
TSCP_FORECAST = {}

def teeRun(cmd):
  if not options.verbose:
    cmd = cmd + ' > %s 2>/dev/null' % TEE_TMP
  else:
    cmd = cmd + ' | tee %s' % TEE_TMP
  printRun(cmd)
  result = open(TEE_TMP).read()

  return result

def filterRestResult(result):
  lines = result.split('\n')

  started = False
  jsonLines = []
  for line in lines:
    if started:
      jsonLines.append(line)
    if line.startswith('{'):
      started = True
      jsonLines.append(line)

  resultJson = json.loads(''.join(jsonLines))
  return resultJson

def filterRestResult(result):
  lines = result.split('\n')

  started = False
  jsonLines = []
  for line in lines:
    if started:
      jsonLines.append(line)
    if line.startswith('{'):
      started = True
      jsonLines.append(line)

  resultJson = json.loads(''.join(jsonLines))
  return resultJson

def envRun(cmd, environment):
  # must be run in a production environment
  #if environment == 'prod':
  #  cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  return teeRun(cmd)

def printRun(cmd):
  if options.verbose:
    print cmd
  os.system(cmd)

def getTimeRange():
  start = int(time.time() * 1000)
  end = start + 1000 * 3600 * 24 * (DAYS - 1) # offline by 1 error on api
  return (start, end)

def makeFabric(environment):
  return '--fabric=%s' % FABRICS[environment]

def sumResult(index, jobsResult, store):
  store[index] = {}
  store[index]['timeSeries'] = {}
  sum = 0
  for value in jobsResult[u'elements'][0][u'timeSeries']:
    store[index]['timeSeries'][value[u'timestamp']] = value[u'value']
    sum +=  int(value[u'value'])
  store[index]['sum'] = sum

def addFilters(filterIndex, filterKey, fields):
  result = 'target.facets[%d].name=%s&' % (filterIndex, filterKey)
  index = 0
  for field in fields:
    result += 'target.facets[%d].values[%d]=%s&' % (filterIndex, index, field)
    index += 1
  return result

def makeFilters(filters):
  index = 0
  filtersExp = ''
  for filter in filters:
    filterKey = filter.split(':')[0]
    filterValue = filter.split(':')[1]
    fields = filterValue.split(',')
    filtersExp += addFilters(index, filterKey, fields)
    index += 1
  return filtersExp

def getFinderName():
  return FINDER_NAME

def makeCampaignType(campaignType):
  return 'campaignType=%s&' % campaignType

def parseRainSliceIdList(result):
  resultLines = result.splitlines()
  sliceList = []
  for line in resultLines:
    if line.find('tscp-forecast') != -1:
      tokens = line.split()
      if tokens[6] == 'ACTIVE':
        sliceList.append(tokens[5])
  return sliceList

def parseRainInstanceHostList(result, environment):
  resultLines = result.splitlines()
  hostList = []
  for line in resultLines:
    if line.find('.linkedin.com') != -1:
      tokens = line.split()
      if tokens[1].find(environment) != -1:
        hostList.append(tokens[0])
  return hostList

def getForecasts(environment):

  # get a list of slice ids from rain
  cmd = CMD_RAIN + ' slice list --product=' + PRODUCT
  result = teeRun(cmd)
  sliceIdList = parseRainSliceIdList(result)
  print('\nFound the following slices:')
  print(sliceIdList)

  # for each slice, get a list of instances that match the environment
  instanceHostList = []
  for sliceId in sliceIdList:
    cmd = CMD_RAIN + ' instance list ' + sliceId
    result = teeRun(cmd)
    instanceHostList += parseRainInstanceHostList(result, environment)

  print('\nFound the following instances:')
  print(instanceHostList)

  # execute a set of queries against tscp-admin-core and store the results
  print('\nExecuting queries against tscp-admin-core:')
  start, end = getTimeRange()
  for campaignType in CAMPAIGN_TYPES:
    for query in QUERIES:
      filtersExp = makeFilters(query)
      url = '%s?q=%s&timeRange.start=%d&timeRange.end=%d&' % (HOST, getFinderName(), start, end) \
            + filtersExp + makeCampaignType(campaignType)
      curliCmd = CMD_CURLI + ' --pretty-print %s \'%s\' -X GET -g -H \'x-restli-protocol-version: 1.0.0\'' % (makeFabric(environment), url)
      result = envRun(curliCmd, environment)
      json = filterRestResult(result)
      sumResult((campaignType + str(QUERIES.index(query))), json, TSCP_ADMIN_CORE)

  # execute the same set of queries against each instance and verify that the results match
  print('\nExecuting queries against tscp-forecast:')
  for instanceHost in instanceHostList:
    for campaignType in CAMPAIGN_TYPES:
      for query in QUERIES:
        filtersExp = makeFilters(query)
        url = '%s://%s:%s%s?q=%s&timeRange.start=%d&timeRange.end=%d&' % (PROTOCOL, instanceHost, PORT, PATH, getFinderName(), start, end) \
              + filtersExp + makeCampaignType(campaignType)
        curliCmd = CMD_CURLI + ' --pretty-print \'%s\' -X GET -g -H \'x-restli-protocol-version: 1.0.0\'' % (url)
        result = envRun(curliCmd, environment)
        json = filterRestResult(result)
        sumResult((instanceHost + campaignType + str(QUERIES.index(query))), json, TSCP_FORECAST)

  # compare results and validate that they match
  print('\nValidating the results of tscp-forecast against tscp-admin-core:')
  failure = False
  DATA_VALIDATION_THRESHOLD = EI_DATA_VALIDATION_THRESHOLD if environment == 'ei' else PROD_DATA_VALIDATION_THRESHOLD;
  for campaignType in CAMPAIGN_TYPES:
    for query in QUERIES:
      print('\n\ncampaignType: ' + campaignType + ', query [' + ' '.join(query) + ']')
      for instanceHost in instanceHostList:
        adminCoreIndex = (campaignType + str(QUERIES.index(query)))
        forecastIndex = (instanceHost + campaignType + str(QUERIES.index(query)))
        match = (TSCP_ADMIN_CORE[adminCoreIndex]['sum'] * (1.0 + DATA_VALIDATION_THRESHOLD) >= TSCP_FORECAST[forecastIndex]['sum']) \
              and (TSCP_ADMIN_CORE[adminCoreIndex]['sum'] * (1.0 - DATA_VALIDATION_THRESHOLD) <= TSCP_FORECAST[forecastIndex]['sum'])
        if not match:
          failure = True
        print(instanceHost + ' - ' + str(match) + ' ' \
          + str(TSCP_ADMIN_CORE[adminCoreIndex]['sum'] * (1.0 - DATA_VALIDATION_THRESHOLD)) + ' <= ' \
          + str(TSCP_FORECAST[forecastIndex]['sum']) + ' <= ' \
          + str(TSCP_ADMIN_CORE[adminCoreIndex]['sum'] * (1.0 + DATA_VALIDATION_THRESHOLD)))

  if failure:
    print('\nFound failures in data quality')
  else:
    print('\nData verification successful')

def printHelp():
  print """
  validateTscpForecast.py ei|prod
  """

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--verbose', default=False, action='store_true', help='show print out')

  (options,args) = parser.parse_args()

  if options.verbose:
    print 'options:', options
    print 'args:', args

  if len(args) < 1 or (args[0] != 'ei' and args[0] != 'prod'):
    printHelp()
    exit(1)

  getForecasts(*args)
