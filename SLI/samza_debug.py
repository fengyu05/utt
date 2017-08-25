#!/usr/bin/python
import sys, os, time, collections, string, random, datetime

# Gloable vairables
_kafka_cluster = 'http://ei3-tracking-rest-vip-1.stg.linkedin.com:10532'
_kafka_schema_id_ad_creative_stats_event = 'cb5475c41989954bb936f289cd56cf2d'
_kafka_schema_id_ad_creative_stats_msg ='0aabc84528ccf9798efea9569b2d3c27'
_millis_in_one_day = 24 * 60 * 60 * 1000

def send_realtieme_cost_event():
  kafka_event_topic = 'tscp_creative_stats_ab_adjusted'
  campaign_ids = _get_campaign_ids()
  for campaign_id in campaign_ids:
    print "\n"
    print "Send realtime cost event with campaignId: %s " % campaign_id
    kafka_event = _make_ad_creative_stats_event(campaign_id, _timestamp(), _random_cost(), _random_cost_adjustment(), _random_tracking_id())
    kafka_event_schema_id = _kafka_schema_id_ad_creative_stats_event
    _send_kfka_evnet(kafka_event_topic, kafka_event_schema_id, kafka_event)
    
def send_rcharge_tracking_event():
  kafka_event_topic = 'ad_system_tracking_event_rcharge'
  campaign_ids = _get_campaign_ids()
  for campaign_id in campaign_ids:
    print "\n"
    print "Send rcharge event with campaignId: %s" % campaign_id
    kafka_event_schema_id = _kafka_schema_id_ad_creative_stats_msg
    kafka_event = _make_ad_creative_stats_msg(campaign_id, _timestamp() - _millis_in_one_day, _random_cost(), _random_cost_adjustment())
    _send_kfka_evnet(kafka_event_topic, kafka_event_schema_id, kafka_event)
    
def send_cost_adjustment_tracking_event():  
  kafka_event_topic = 'ad_system_tracking_event_costadjustment'
  campaign_ids = _get_campaign_ids()
  for campaign_id in campaign_ids:
    print "\n"
    print "Send cost adjustment event with campaignId %s " % campaign_id
    kafka_event_schema_id = _kafka_schema_id_ad_creative_stats_msg
    kafka_event = _make_ad_creative_stats_msg(campaign_id, _timestamp() - _millis_in_one_day, _random_cost(), _random_cost_adjustment())
    _send_kfka_evnet(kafka_event_topic, kafka_event_schema_id, kafka_event)

def _get_campaign_ids():
  # Check if campaign_ids provided by user, use random one if not
  if options.campaigns != None:
    campaign_ids = _parse_campaigns(options.campaigns)
  else:
    campaign_ids = (_random_campaign_id(),)

  # Write campaignIds into file for validation
  if (options.output != None):
    with open(options.output, "a") as campaign_id_file:
      for id in campaign_ids: 
        campaign_id_file.write("%s" % id)
        campaign_id_file.write(",")

  #return campaign_id
  return campaign_ids
      

def _parse_campaigns(campaign_list):
  return campaign_list.split(',')

def _random_tracking_id():
  return ''.join(random.choice(string.lowercase) for x in range(16))

def _timestamp():
  return int(round(time.time() * 1000))

def _random_campaign_id():
  return random.getrandbits(30)

def _random_cost():
  return abs(random.randrange(100) + random.random())

def _random_cost_adjustment():
  return random.randrange(100) + random.random()
  
def _make_ad_creative_stats_event(campaign_id, timestamp, cost, cost_adjustment, tracking_id):
    print 'generate AdCreativeStatsEvent: campaignId:%s, timestamp:%s, cost:%s, costAdjustment:%s, trackingId:%s' %(campaign_id, timestamp, cost, cost_adjustment, tracking_id)
    ad_creative_stat_event = """{"header":{"memberId":-1,"viewerUrn":null,"applicationViewerUrn":null,"csUserUrn":null,"time":%s,"server":"lva1-app1160","service":"sas-campaign","environment":{"string":"EI3"},"guid":"0123456789012345","treeId":{"fixed_16":"0123456789123456"},"requestId":{"int":0},"impersonatorId":null,"version":null,"instance":null,"appName":null,"testId":null,"testSegmentId":null,"auditHeader":{"KafkaAuditHeader":{"time":1453847539163,"server":"lva1-app1160","instance":{"string":"lva1-app1160_sas-campaign"},"appName":"sas-campaign","messageId":"1234567890123456"}},"pageInstance":null},"advertiserId":510282630,"campaignId":%s,"creativeId":95789402,"daysSinceEpoch":16826,"weeksSinceEpoch":2403,"monthsSinceEpoch":552,"campaignType":5,"impressionCount":1,"clickCount":0,"otherClickCount":0,"conversionCount":0,"costInCurrency":0.008619999656677245,"currency":"USD","cost":%s,"costAdjustment":%s,"adTrackingId":{"string":"%s"}}""" %(timestamp, campaign_id, cost, cost_adjustment, tracking_id)
    return ad_creative_stat_event

def _make_ad_creative_stats_msg(campaign_id, timestamp, cost, cost_adjustment):
    print 'generate AdCreativeStatsMsg: campaignId:%s, timestamp:%s, cost:%s, costAdjustment:%s' %(campaign_id, timestamp, cost, cost_adjustment)
    ad_creative_stat_msg = """{"header":{"memberId":0,"viewerUrn":null,"applicationViewerUrn":null,"csUserUrn":null,"time":1453772622000,"server":"eat1-app482","service":"sasproc","environment":{"string":"EI3"},"guid":"ipad412345678901","treeId":null,"requestId":null,"impersonatorId":null,"version":null,"instance":null,"appName":null,"testId":null,"testSegmentId":null,"auditHeader":{"KafkaAuditHeader":{"time":1453768948807,"server":"eat1-app482","instance":{"string":"eat1-app482_sasproc"},"appName":"sasproc","messageId":"1234567890123456"}},"pageInstance":null},"trackingId":"[-111,23, -2, 85, -74, -19, -125, -101, 115, -22, 68, -74, -103, -57, -105,-51]","advertiserUrn":"urn:li:sponsoredAccount:511257984","campaignUrn":"urn:li:sponsoredCampaign:%s","creativeUrn":"urn:li:sponsoredCreative:0","timestamp":%s,"campaignType":14,"impressionCount":19531,"clickCount":109,"otherClickCount":14,"conversionCount":0,"costInCurrency":14796.71,"currency":"CNY","cost":%s,"costAdjustment":%s}""" %(campaign_id, timestamp, cost, cost_adjustment)
    return ad_creative_stat_msg

def _send_kfka_evnet(topic, schema_id, kafka_event):  
  url = '%s/tracking-rest/kafka/topics/%s/?schemaId=%s' %(_kafka_cluster, topic, schema_id)
  curli_cmd = 'curl -X POST -H \"Content-Type: application/json\" %s -d \'%s\'' %(url, kafka_event)
  print curli_cmd
  result = envRun(curli_cmd)

def envRun(cmd):
  env = options.env
  cmd = cmd
  if env.startswith('prod-'):
    cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  os.system(cmd)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-e', '--event', default='realtime')
  parser.add_option('-t', '--times', default = 1)
  parser.add_option('-c', '--campaigns')
  parser.add_option('-o', '--output')
  parser.add_option('--env', default='', help='env')


  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  for i in range(int(options.times)):
    if options.event == 'realtime':
      send_realtieme_cost_event()
    elif options.event == 'rcharge':
      send_rcharge_tracking_event()
    elif options.event == 'costadjust':
      send_cost_adjustment_tracking_event()
    else:
      print 'Invalid event name'
    print '\n'
    print 'Send %s events.' % i
