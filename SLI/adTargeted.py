#!/usr/bin/python
from restli import *
import random
import uuid
import time
import urllib

options = {}

# RESOURCE
TARGETED_RESOURCE = "adTargeted"

CAMPAIGN_TYPES = ["SPONSORED_STATUS_UPDATES_V2", "TEXT_AD"]

'''
Ex: geos:na.us skills:33049,50188 langs:en followCampanies:!247338
'''
def makeTargets(targets):
  targetFacet = []
  targetSpecs = targets.split(' ')
  for spec in targetSpecs:
    targetItem = {}
    specFileds = spec.split(':')
    key = specFileds[0]
    values = specFileds[1]
    valueFileds = values.split(',')
    targetItem['name'] = key
    targetItem['values'] = valueFileds
    targetFacet.append(targetItem)
  return targetFacet

def makeCampaignSpec(campaign):
  return urllib.quote(campaign.__repr__().replace('\'', '"').replace('False', 'false').replace('True', 'true'))

def getAdTargeted(campaignType="SPONSORED_STATUS_UPDATES_V2", geo="na.us", targets='', bidType='CPC'):
  data = {
    "campaign": {
      "allowScin":True,
      "status":"ACTIVE",
      "locale":{"language":"en","country":"US"},
      "versionTag":"11332139",
      "parent":"urn:li:sponsoredAccount:510313197",
      "spendLimits":[{"type":"TOTAL","spend":{"amount":"69.1","currencyCode":"USD"}}],
      "type": campaignType,
      "spammer":False,
      "reference":"urn:li:job:2504816",
      "id":317551372,
      "servingStatus":"RUNNABLE",
      "costType": bidType,
      "allowOffsiteDelivery":False,
      "creativeSelection":"OPTIMIZED",
      "unitCost":{"amount":"2.91","currencyCode":"USD"},
      "runSchedule":{"start":1400630400000,"end":1403222400000},
      "name":"Software Test Engineer 61YwjC5v",
      "partitionId":510313197,
      "stamps":{
        "lastModified":{"time":1400707516000,"actor":"urn:li:unknown:0"},
        "created":{"time":1400707392000,"actor":"urn:li:member:0"}
        },
      "collectLeads":False,
      "targets":{"dataVersion":4,"facets":[
        {"values":[geo],"name":"geos"},
        {"values":["en"],"name":"langs"}
        ]}}
  }

  if targets:
    print 'Override targets'
    data['campaign']['targets']['facets'] = makeTargets(targets)

  print data['campaign']['targets']['facets']

  request = FinderRequest(TARGETED_RESOURCE, 'search', {'campaign_spec' : makeCampaignSpec(data['campaign'])})
  if options.host:
    request.setLocalResource("http://%s/sas-campaign/resources/adCampaigns" % options.host)
  elif options.local:
    request.setLocalResource("http://localhost:%s/sas-campaign/resources/adCampaigns" % options.port)

  if options.memberId:
    request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % options.memberId)

  if options.concurrent:
    request.setConcurrent(True)

  request.setEnv(options.env)
  request.execute()

def main(args):
  getAdTargeted(options.campaignType, 'na.us', options.targets, options.bidType)


if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='', help='env')
  parser.add_option('-t', '--time', type=float, default=1.0, help='sleep time')
  parser.add_option('-l', '--local', action="store_true", help='localhost')
  parser.add_option('-m', '--memberId', default="", help='memberId')
  parser.add_option('--host', default="", help='host name')
  parser.add_option('-p', '--port', default=9999, help='port')
  parser.add_option('--ct', dest='campaignType', default='SPONSORED_STATUS_UPDATES_V2', help='campaignType')
  parser.add_option('--bt', dest='bidType', default='CPC', help='bid type')
  parser.add_option('-f', '--targets', dest='targets', default='', help='targets')
  parser.add_option('--concurrent', action="store_true")

  global options
  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  main(args)
