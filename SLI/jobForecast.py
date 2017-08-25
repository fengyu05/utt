#!/usr/bin/python
import sys, os, time
import urllib
import json
import subprocess
import urllib
import restli

D2_RESOURCE = 'jobPerformanceForecasts'

options ={}
args = []

FINDER_NAME = 'criteria'
CURLI = '/usr/local/linkedin/bin/curli'

TEE_TMP = '/tmp/tee.job_ac'

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


def makeFabric():
  if options.env:
    return '--fabric=%s' % options.env
  else:
    return ''


def getFinderName():
  return FINDER_NAME

def getResource():
  return D2_RESOURCE

def makeGeo(geoOption):
  fields = geoOption.split('.')
  return {
      "countryGroups": filter(None, ['urn:li:countryGroup:%s' % fields[0] if len(fields) > 0 else None]),
      "countries": filter(None, ['urn:li:country:%s' % fields[1] if len(fields) > 1 else None]),
      "states": filter(None, ['urn:li:state:(urn:li:country:%s,%s)' % (fields[1], fields[2]) if len(fields) > 2 else None]),
      "regions": filter(None, ['urn:li:region:%s' % fields[3] if len(fields) > 3 else None]),
      }


def makeFacets(options, urn):
  fields = options.split(',')
  return map(lambda x: 'urn:li:%s:%s' %(urn, x), fields)

def makeYOE(yoeOption):
  fields = yoeOption.split('-')
  return {
      "start": int(fields[0]),
      "end": int(fields[1]),
      }

def makeTimeRange(dayOption):
  start = int(time.time() * 1000)
  end = start + 1000 * 3600 * 24 * (dayOption - 1) # offline by 1 error on api
  return {
      "start": start,
      "end": end
      }


def getForecasts():
    data = {
        'targetingSegments' : {
          "excludedFacets" : { },
          "includedFacets" : {
            "functions" : [ ],
            "companies" : [ ],
            "industries" : [ ],
            "skills" : [ ],
            "titles" : [ ],
            "profileLocations" : {
              "countryGroups" : [ 'urn:li:countryGroup:na'],
              "countries" : ['urn:li:country:us'],
              "states" : [ ],
              "regions" : [ ],
              }
            },
          },
        'metric': options.metric,
        'timeRange' : makeTimeRange(options.day),
        'jobPostingInfo': {}
      }

    if options.geo:
      data['targetingSegments']['includedFacets']['profileLocations'] = makeGeo(options.geo)
    if options.functions:
      data['targetingSegments']['includedFacets']['functions'] = makeFacets(options.functions, 'function')
    if options.companies:
      data['targetingSegments']['includedFacets']['companies'] = makeFacets(options.companies, 'company')
    if options.industries:
      data['targetingSegments']['includedFacets']['industries'] = makeFacets(options.industries, 'industry')
    if options.skills:
      data['targetingSegments']['includedFacets']['skills'] = makeFacets(options.skills, 'skill')
    if options.titles:
      data['targetingSegments']['includedFacets']['titles'] = makeFacets(options.titles, 'title')
    if options.yoe:
      data['targetingSegments']['includedFacets']['yearsOfExperienceRange'] = makeYOE(options.yoe)

    print 'Targeting data'
    print data

    query = restli.FinderRequest(getResource(), getFinderName(), data)

    query.setEnv(options.env)
    if options.local:
      query.setLocalResource("http://localhost:2634/jobs-marketplace-forecasting-restli/%s" % D2_RESOURCE)
    query.enableV2()
    #print query.getCurli()
    query.execute()


if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='ei-lca1', help='env')
  parser.add_option('-d', '--day', type='int', default='7', help='')
  parser.add_option('-m', '--metric', default='UNIQUE_APPLY', help='')
  parser.add_option('--geo', default='', help='geo')
  parser.add_option('--functions', default='', help='')
  parser.add_option('--companies', default='', help='')
  parser.add_option('--industries', default='', help='')
  parser.add_option('--titles', default='', help='')
  parser.add_option('--skills', default='', help='')
  parser.add_option('--yoe', default='', help='')
  parser.add_option('--mute', default=False, action='store_true', help='mute print out')
  parser.add_option('--skip_portal', default=False, action='store_true', help='skip portal')
  parser.add_option('--local', default=False, action='store_true', help='local host model')

  (options,args) = parser.parse_args()

  if not options.mute:
    print 'options:', options
    print 'args:', args

  getForecasts(*args)
