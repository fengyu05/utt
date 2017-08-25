#!/usr/bin/python
import sys, os, time
import urllib
import json
import subprocess
import urllib

D2_HOST = 'd2://adForecasts'
API_HOST = 'https://api.linkedin.com/v2/adSupplyForecasts'

AUTH_HEADER = '\'Authorization:Bearer AQU07GpFzG39SZaNzmQ63B_CWy8hkoff2zHOWyNp0Pv4Y2_Xj5awaAawwv5AeEK5fbk2GRs9eo7wxueb5WkvBJKq2fDi6GReH1xqavgjqsEe89B1tNlBlvQ_2Yecwn_fJcppTj2k8J8cnc-qNh62Dz-Qg6VVVHZW4qlMUujvgwCKZePhg_M\''

options ={}
args = []

CAMPAIGN_TYPES = {
    'im' : 'SPONSORED_INMAILS',
    'inmail' : 'SPONSORED_INMAILS',
    'su' : 'SPONSORED_STATUS_UPDATES_V2',
    'scin' : 'SPONSORED_STATUS_UPDATES_V2',
    'native' : 'DYNAMIC'
}


CAMPAIGN_TYPES_API = {
    'su' : 'SPONSORED_UPDATES',
}

ADSIZE = {
    '300x250' : True,
    '17x700' : True,
    '160x600' : True,
    }

FINDER_NAME = 'supplyCriteria'
API_FINDER_NAME = 'criteria'
TOTAL_FINDER_NAME = 'totalSupplyCriteria'
EXTERNAL_FINDER_NAME = 'supplyCriteriaWithTargetSpec'
CURLI = '/usr/local/linkedin/bin/curli'

TEE_TMP = '/tmp/tee.fcst'

def teeRun(cmd):
  if options.mute:
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

def envRun(cmd, prod=False):
  env = options.env
  cmd = cmd
  if (not options.skip_portal) and (env.startswith('prod-') or prod):
    cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  return teeRun(cmd)

def printRun(cmd):
  if not options.mute:
    print cmd
  os.system(cmd)

def pipeRun(cmd):
  if not options.mute:
    print cmd
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            shell=True)
  output, error = p.communicate()
  if not options.mute:
    print output
    print error
  return output

def getTimeRange():
  start = int(time.time() * 1000)
  end = start + 1000 * 3600 * 24 * (options.day - 1) # offline by 1 error on api
  return (start, end)

def makeGeo():
  geos = 'target.facets[0].name=geos&' +\
         'target.facets[0].values[0]=%s&' % options.geo
  return geos

def makeBid():
  if options.bid and not options.total:
    bids = options.bid.split(':')
    bid = bids[0]
    currencyCode = len(bids) > 1 and bids[1] or 'USD'
    return 'competingBid.bidType=%s&competingBid.bidPrice.currencyCode=%s&competingBid.bidPrice.amount=%s&' % (options.bidType, currencyCode, bid)
  else:
    return ''

def makeFabric():
  if options.env:
    return '--fabric=%s' % options.env
  else:
    return ''

def makeExtraHeader():
  if options.api:
    return ' --header %s -i' % AUTH_HEADER
  else:
    return ''


def sumResult(jobsResult):
  sum = 0
  for value in jobsResult[u'elements'][0][u'timeSeries']:
    sum +=  int(value[u'value'])
  return sum

def addFilters(filterIndex, filterKey, fields):
  result = 'target.facets[%d].name=%s&' % (filterIndex, filterKey)
  index = 0
  for field in fields:
    result += 'target.facets[%d].values[%d]=%s&' % (filterIndex, index, field)
    index+=1
  return result

def makeFilters():
  filterSpec = options.filters and options.filters or options.targets or options.adsize or options.adzone
  if filterSpec:
    index = 0
    filtersExp = ''
    if options.filters:
      filters = options.filters.split(' ')
      for filter in filters:
        index += 1
        filterKey = filter.split(':')[0]
        filterValue = filter.split(':')[1]
        fields = filterValue.split(',')
        filtersExp += addFilters(index, filterKey, fields)
    if options.adsize:
      filterKey = 'ct_adsize'
      filterValue = options.adsize
      index += 1
      filtersExp += addFilters(index, filterKey, filterValue)
    if options.adzone:
      index += 1
      filterKey = 'ct_adzone'
      filterValue = options.adzone
      filtersExp += addFilters(index, filterKey, filterValue)
    return filtersExp
  else:
    return ''

def makeFrequencyCaps():
  if options.fcaps and not options.total:
    frequency = options.fcaps.split('-')[0]
    duration = options.fcaps.split('-')[1]
    return 'frequencyCaps[0].policyType=ACROSS_CAMPAIGNS&frequencyCaps[0].frequency=%s&frequencyCaps[0].timeSpan.duration=%s&frequencyCaps[0].timeSpan.unit=DAY' %(frequency, duration)
  return ''

def getFinderName():
  if options.external:
    return EXTERNAL_FINDER_NAME
  elif options.api:
    return API_FINDER_NAME
  elif options.total:
    return TOTAL_FINDER_NAME
  else:
    return FINDER_NAME

def getHostName():
  if options.api:
    return API_HOST
  return D2_HOST

def makeTargetSpec():
  return urllib.quote("{" +\
      "'geos' : ['na.us']" +\
          "}")

def makeApiTargetGeoSpec():
  return 'urn:li:country:ca'

def makeTargetParam():
  if options.api:
    return 'target.includedTargetingFacets.locations[0]=%s&' % makeApiTargetGeoSpec()
  elif options.external:
    return 'targetSpec=%s&' % makeTargetSpec()
  else:
    return 'target.dataVersion=4&' + makeGeo() + makeFilters()

def makeCampaignType(campaignType):
  if options.api:
    return 'campaignType=%s&' % CAMPAIGN_TYPES_API[campaignType]
  else:
    return 'campaignType=%s&' % CAMPAIGN_TYPES[campaignType]

def makeRoadBlockParam():
  if options.rb and not options.total:
    return '&enableRoadBlockerDiscountFactor=true'
  else:
    return ''

def buildFilters(resultJson):
    facets = resultJson['targets']['facets']
    filtersExp, index = "", 0
    for facet in facets:
        filterKey = facet['name']
        filterValue = facet['values']

        if filterKey == 'ct_adsize':
            filterValue = [v[5:].replace('_', 'x') for v in filterValue]

        filtersExp += addFilters(index, filterKey, filterValue)
        index += 1
    return filtersExp

def getForecasts(campaignType):
    filtersExp = ""
    if options.cid:
        query_target_url =  'd2://adCampaigns/%s?fields=targets' % options.cid
        curliCmd = CURLI + ' --pretty-print --fabric=%s \'%s\' -X GET -g ' % (options.cenv, query_target_url)
        result = envRun(curliCmd, True)
        resultJson = filterRestResult(result)
        filtersExp = buildFilters(resultJson)

    if not filtersExp:
        filtersExp = makeTargetParam()

    start, end = getTimeRange()
    url = '%s?q=%s&timeRange.start=%d&timeRange.end=%d&' % (getHostName(), getFinderName(), start, end) + \
          filtersExp + makeCampaignType(campaignType) + makeBid() + makeFrequencyCaps() + makeRoadBlockParam()

    curliCmd = CURLI + ' --pretty-print %s \'%s\' %s -X GET -g -i' % (makeFabric(), url, makeExtraHeader())
    result = envRun(curliCmd)
    result = filterRestResult(result)
    print sumResult(result)

def printHelp():
  print """
  getForecasts.py im|su [--env=prod-lva1] [-d 7] [-g na.us] [-b 2.7:USD] [-t CPC|CPM] [--fcaps 7-7 (time-day)]
  """

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='ei-lca1', help='env')
  parser.add_option('-d', '--day', type='int', default=7, help='day')
  parser.add_option('-g', '--geo', default='na.us', help='geo')
  parser.add_option('-b', '--bid', default='', help='bid')
  parser.add_option('-t', '--bidType', default='CPC', help='bid type')
  parser.add_option('-f', '--filters', default='', help='filters')
  parser.add_option('--targets', default='', help='targets')
  parser.add_option('--rb', action='store_true', help='road blocker')
  parser.add_option('-c', '--fcaps', default='', help='frequency cap')
  parser.add_option('-e', '--external', action='store_true', help='use external')
  parser.add_option('--total', action='store_true', help='return total supply')
  parser.add_option('--adsize', default='', help='ad size')
  parser.add_option('--adzone', default='', help='ad zone')
  parser.add_option('--cid', default='', help='campaign id')
  parser.add_option('--cenv', default='prod-lva1', help='campaign env')
  parser.add_option('--mute', default=False, action='store_true', help='mute print out')
  parser.add_option('--skip_portal', default=False, action='store_true', help='skip portal')
  parser.add_option('--api', default=False, action='store_true', help='api call')

  (options,args) = parser.parse_args()

  if not options.mute:
    print 'options:', options
    print 'args:', args

  if len(args) < 1:
    printHelp()
    exit(1)

  getForecasts(*args)
