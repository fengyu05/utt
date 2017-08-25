#!/usr/bin/python
import sys, os, time, collections, string, random, datetime

"""
Espresso query functions.
@author xozhang
"""

# Espresso routers
ROUTER = {
  "ei-lca1" : "https://lca1-espresso-router-router-ssl-mt1-vip.stg.linkedin.com:11937",
  "ei-ltx1" : "https://ltx1-espresso-router-router-ssl-mt1-vip.stg.linkedin.com:11937"   
  }

# SSH command 
# please use: `id-tool grestin sign` to generate certificaiton

SSH_OPTION = "--cert ./identity.cert --key ./identity.key --cacert /etc/riddler/riddler-ca.cert --ciphers rsa_null_md5 -k"

#===========================================================
# Tables Names
#===========================================================
TABLE_ACCOUNT = 'account'
TABLE_ACCOUNT_STATS = 'accountStats'
TABLE_CAMPAIGN_GROUP = 'campaignGroup'
TABLE_CAMPAIGN_GROUP_STATS = 'campaignGroupStats'
TABLE_CAMPAIGN = 'campaign'
TABLE_CAMPAIGN_STATS = 'campaignStats'
TABLE_CREATIVE ='creative'
TABLE_CREATIVE_STATS = 'creativeStats'

TABLE_NAMES = [ TABLE_ACCOUNT, TABLE_ACCOUNT_STATS, TABLE_CAMPAIGN_GROUP, TABLE_CAMPAIGN_GROUP_STATS, TABLE_CAMPAIGN, TABLE_CAMPAIGN_STATS, TABLE_CREATIVE, TABLE_CREATIVE_STATS ]

#===========================================================
# Accounts table avro template
#===========================================================
account_avro_template='{"status":"ACTIVE","servingStatus":"RUNNABLE","currencyCode":"USD","spendLimits":[{"type":"DAILY","spend":{"currencyCode":"USD","amount":"%s"}}, {"type":"TOTAL","spend":{"currencyCode":"USD","amount":"%s"}}],"spendCaps": [{"type": "DAILY", "spend": {"currencyCode": "USD", "amount": "%s"}}]}'

#===========================================================
# AccountStats/CampaignGroupStats/CampaignStats/CreativeStats
# table avro template
#===========================================================
"""
Complete schema for later reference:
{"impressions":123805,"clicks":4458,"clicksOther":0,"conversions":0,"cost":7008.582614679162,"costInUSD":7008.582614679162,"currency":"USD","lastUpdateTime":1479752349389,"overDeliveryAdjustment":0.0,"lateEventAdjustment":0.0,"roundingErrorAdjustment":0.0,"sponsoredLeads":0,"viralLeads":0}
"""
stats_avro_template='{"cost":%s,"costInUSD":%s,"currency":"USD"}'

# used only when creating a new entry
stats_avro_template_create='{"impressions":123805,"clicks":4458,"clicksOther":0,"conversions":0,"cost":%s,"costInUSD":%s,"currency":"USD","lastUpdateTime":1479752349389,"overDeliveryAdjustment":0.0,"lateEventAdjustment":0.0,"roundingErrorAdjustment":0.0,"sponsoredLeads":0,"viralLeads":0}'

#===========================================================
# CampaignGroup table avro template
#===========================================================
"""
CampaignGroup table complete schema:
"""
campaign_group_avro_template='{"totalBudget":"%s","currency":"USD","lastUpdateTime":1485216505000}'

# used for creating a new entry
campaign_group_avro_template_create = '{"totalBudget":"%s","currency":"USD","lastUpdateTime":1485216505000}'

#===========================================================
# Campaign table avro template
#===========================================================
"""
Complete schema for later reference:
{"versionTag":"4","parent":"urn:li:sponsoredAccount:512308451","name":"Adv2ad34424-c594-4463-a3d0-d1886aea7504","type":"CUSTOM","status":"PAUSED","servingStatus":"STOPPED","spendLimits":[{"type":"DAILY","spend":{"currencyCode":"USD","amount":"0.0"}},{"type":"TOTAL","spend":{"currencyCode":"USD","amount":"0.0"}}],"unitCost":{"currencyCode":"USD","amount":"0.0"},"floor":null,"costType":"CPC","creativeSelection":"OPTIMIZED","targets":{"dataVersion":4,"facets":[{"name":"geos","values":["na.us"]},{"name":"langs","values":["en"]}]},"runSchedule":{"start":1479499481541,"end":1479585881541},"locale":{"language":"en","country":"US","variant":null},"leads":null,"reference":"urn:li:company:62787","billingParentReference":"urn:li:finXsm:123","billingReference":null,"allowOffsiteDelivery":false,"collectLeads":true,"spammer":false,"allowScin":true,"stamps":{"created":{"time":1479413081000,"actor":"urn:li:member:100277677"},"lastModified":{"time":1479429684170,"actor":"urn:li:unknown:0"},"deleted":null},"source":null,"roadBlockType":"NONE"}
"""
campaign_avro_template_create='{"versionTag":"4","parent":"urn:li:sponsoredAccount:512308451","name":"Adv2ad34424-c594-4463-a3d0-d1886aea7504","type":"CUSTOM","status":"PAUSED","servingStatus":"STOPPED","spendLimits":[{"type":"DAILY","spend":{"currencyCode":"USD","amount":"%s"}},{"type":"TOTAL","spend":{"currencyCode":"USD","amount":"%s"}}],"unitCost":{"currencyCode":"USD","amount":"0.0"},"floor":null,"costType":"CPC","creativeSelection":"OPTIMIZED","targets":{"dataVersion":4,"facets":[{"name":"geos","values":["na.us"]},{"name":"langs","values":["en"]}]},"runSchedule":{"start":1479499481541,"end":1479585881541},"locale":{"language":"en","country":"US","variant":null},"leads":null,"reference":"urn:li:company:62787","billingParentReference":"urn:li:finXsm:123","billingReference":null,"allowOffsiteDelivery":false,"collectLeads":true,"spammer":false,"allowScin":true,"stamps":{"created":{"time":1479413081000,"actor":"urn:li:member:100277677"},"lastModified":{"time":1479429684170,"actor":"urn:li:unknown:0"},"deleted":null},"source":null,"roadBlockType":"NONE"}'
campaign_avro_template='{"status":"ACTIVE","servingStatus":"RUNNABLE","spendLimits":[{"type":"DAILY","spend":{"currencyCode":"USD","amount":"%s"}},{"type":"TOTAL","spend":{"currencyCode":"USD","amount":"%s"}}]}'

#===========================================================
# Creative table avro template
#===========================================================
"""
Complete schema for later reference:
{"versionTag":"3","parent":"urn:li:sponsoredCampaign:325809334","type":"SPONSOREDSTATUSUPDATES","status":"CANCELLED","servingStatus":"STOPPED","review":{"reviewStatus":"APPROVED","rejectionCode":null,"explanation":null},"reference":"urn:li:activity:6093533960611045376","billingReference":null,"preview":null,"variables":{"href":null,"subType":{"activity":"urn:li:activity:6093533960611045376","darkPost":false}},"deferredReview":false,"badContent":false,"contentChecked":false,"darkPost":false,"stamps":{"created":{"time":1479243899000,"actor":"urn:li:member:99840755"},"lastModified":{"time":1479243899000,"actor":"urn:li:unknown:0"},"deleted":null}}
"""
creative_avro_template='TBD'

# Account Status
ACCT_STATUS_ACTIVE = 'ACTIVE'
ACCT_STATUS_PENDING = 'PENDING_CANCELLATION'
ACCT_STATUS_CANCEL = 'CANCELLED'

# Granularity
GRANU_DAY = 'day'
GRANU_MONTH = 'month'
GRANU_LIFE = 'lifetime'

#===========================================================
# Account table read/write
#===========================================================
def _build_account_url():
  """
  Build account read url.
  Required prameters:
    accountId
  """
  account_id = options.acct
  print '********************'
  return '/Accounts/%s' % (account_id)

def _build_account_write_body():
  """
  Build account write body.
  Support parameter:
    daily budget
  """
  budget = options.budget
  granu = options.granu
  return account_avro_template % (budget, budget, budget)
  #if granu == 'lifetime':
  #elif granu == 'day':
  #  return account_avro_template_daily % (budget, budget)

#===========================================================
# AccountStats table read/write
#===========================================================
# Special day value when granularity as lifetime
GRANU_LIFETIME_DAY_VALUE = '-62135769600000'

# default day value when granualrity is day
GRANU_DAY_DEFAULT_DAY = '1475280000000'

def _build_account_stats_url():
  """
  Build accountStatus table read url.
  Key:
    accountId,day,granularity,colo
  """
  account_id = options.acct
  granu = options.granu
  day = options.day

  if granu == 'day':
    granu = GRANU_DAY
    # today
    day = options.day
    #day=int(time.time() * 1000 / 86400000) * 86400000

  elif granu == 'lifetime':
    granu = GRANU_LIFE
    day = GRANU_LIFETIME_DAY_VALUE

  elif granu == 'month':
    granu = GRANU_MONTH
    # TODO: add default value for month
  else:
    raise Excepption('Invalid input for granularity')

  return '/AccountStats/%s/%s/%s/EI' % (account_id, day, granu)

#===========================================================
# Stats table write body
#===========================================================
def _build_stats_table_write_body():
  """
  Build accountStats table write body.
  Supported parameter:
    cost
  """
  cost = options.cost
  if options.create:
    return stats_avro_template_create % (cost, cost)
  else:
    return stats_avro_template % (cost, cost)

#===========================================================
# CampaignGroup table read/write queries.
#===========================================================
def _build_campaign_group_url():
  """
  Build campaignGroup table read url.
  Required parameters:
    accountId
    campaignGroupId
  """
  account_id = options.acct
  camp_group_id = options.campgroup
  print 'account_id' + account_id
  print 'campaign_group_id' + camp_group_id
  
  return '/CampaignGroups/%s/%s' % (account_id, camp_group_id)

def _build_campaign_group_write_body():
  """
  Build campaignGroup table write body.
  key: 
    accountId, campaignGroupId
  supported parameter:
    budget
  """
  budget = options.budget
  if options.create:
      return  campaign_group_avro_template_create % (budget)
  else:
      return campaign_group_avro_template % (budget)

#===========================================================
# CampaignGroupStats table read/write queries.
#===========================================================
def _build_campaign_group_stats_url():
  """
  Build accountStatus table read url.
  Key:
    accountId,day,granularity,colo
  """
  account_id = options.acct
  campaign_group_id = options.campgroup
  granu = options.granu
  day = options.day

  if granu == 'day':
    granu = GRANU_DAY
    # today
    day=int(time.time() * 1000 / 86400000) * 86400000

  elif granu == 'lifetime':
    granu = GRANU_LIFE
    day = GRANU_LIFETIME_DAY_VALUE

  elif granu == 'month':
    granu = GRANU_MONTH
    # TODO: add default value for month
  else:
    raise Excepption('Invalid input for granularity')

  return '/CampaignGroupStats/%s/%s/%s/%s/EI' % (account_id, day, granu, campaign_group_id)
  return '/CampaignStats/%s/%s/%s/%s/EI' % (account_id, day, granu, campaign_id)

#===========================================================
# Campaign table read/write queries.
#===========================================================
def _build_campaign_url():
  """
  Build campaign table read url.
  Required parameters:
    accountId
    campaignId
  """
  account_id = options.acct
  campaign_id = options.camp
  
  return '/Campaigns/%s/%s' % (account_id, campaign_id)

def _build_campaign_write_body():
  """
  Build campaign write body.
  Key:
    accountId, campaignId
  Supported parameter:
    daily budget
  """
  budget = options.budget
  if options.create:
    return campaign_avro_template_create  % (budget, budget)
  else:
    return campaign_avro_template % (budget, budget)

#===========================================================
# CampaignStats table read/write queries.
#===========================================================
def _build_campaign_stats_url():
  """
  Build AaccountStats table read url.
  Key:
    accountId,campaignId,day,granularity,colo
  """
  account_id = options.acct
  campaign_id = options.camp

  granu = options.granu
  day = options.day

  if granu == 'day':
    granu = GRANU_DAY
    # today
    #day=int(time.time() * 1000 / 86400000) * 86400000

  elif granu == 'lifetime':
    granu = GRANU_LIFE
    day = GRANU_LIFETIME_DAY_VALUE

  elif granu == 'month':
    granu = GRANU_MONTH
    # TODO: add default value for month
  else:
    raise Excepption('Invalid input for granularity')

  return '/CampaignStats/%s/%s/%s/%s/EI' % (account_id, day, granu, campaign_id)

#===========================================================
# Creative table read/write queries.
#===========================================================
def _build_creative_url():
  """
  Build creative table read url.
  Required parameters:
    creativeId
  """
  account_id = options.acct
  campaign_id = options.camp
  creative_id = options.crtv
  return '/Creatives/%s/%s/%s' % (account_id, campaign_id, creative_id)

#===========================================================
# CreativeStats table read/write queries.
#===========================================================
def _build_creative_stats_url():
  """
  Build CreativeStats table read url.
  Key:
    accountId,campaignId,day,granularity,colo
  """
  account_id = options.acct
  campaign_id = options.camp
  creative_id = options.crtv

  granu = options.granu
  day = options.day

  if granu == 'day':
    granu = GRANU_DAY
    # today
    day=int(time.time() * 1000 / 86400000) * 86400000

  elif granu == 'lifetime':
    granu = GRANU_LIFE
    day = GRANU_LIFETIME_DAY_VALUE

  elif granu == 'month':
    granu = GRANU_MONTH
    # TODO: add default value for month
  else:
    raise Excepption('Invalid input for granularity')

  return '/CreativeStats/%s/%s/%s/%s/%s/EI' % (account_id, day, granu, campaign_id, creative_id)

#===========================================================
# CampaignStatsCache
#===========================================================
def _build_campaign_stats_cache_url():
  """
  Build campaign stats cache
  Required parameters:
    accountId
    campaignId
  """
  account_id = options.acct
  campaign_id = options.camp
  return '/CampaignStatsCache/%s/%s' % (account_id, campaign_id)


#===========================================================
# Build queries.
#===========================================================
def _build_cluster_url():
  return '/TSCP'

def _get_router():
  env = options.env
  return ROUTER[env]

def _build_read_query():
  table = options.table
  url = None
  if table == 'account':
    url = _build_account_url()
  elif table== 'campaignGroup':
    url = _build_campaign_group_url()
  elif table == 'campaign':
    url = _build_campaign_url()
  elif table == 'creative':
    url =  _build_creative_url()
  elif table == 'accountStats':
    url = _build_account_stats_url()
  elif table == 'campaignGroupStats':
    url = _build_campaign_group_stats_url()
  elif table == 'campaignStats':
    url = _build_campaign_stats_url()
  elif table == 'creativeStats':
    url = _build_creative_stats_url()
  elif table == 'campaignStatsCache':
    url = _build_campaign_stats_cache_url()
  else:
    print "Unsupported table name: %s" % table
    return
  return _build_cluster_url() + url

def _build_write_query():
  table = options.table
  key = None
  body = None
  if table == TABLE_ACCOUNT:
    key = _build_account_url()
    body = _build_account_write_body()

  elif table == TABLE_ACCOUNT_STATS:
    key = _build_account_stats_url()
    body = _build_stats_table_write_body()

  elif table == TABLE_CAMPAIGN_GROUP:
    key = _build_campaign_group_url()
    body = _build_campaign_group_write_body()

  elif table == TABLE_CAMPAIGN_GROUP_STATS:
    key = _build_campaign_group_stats_url()
    body = _build_stats_table_write_body()

  elif table == TABLE_CAMPAIGN:
    key = _build_campaign_url()
    body = _build_campaign_write_body()

  elif table == TABLE_CAMPAIGN_STATS:
    key = _build_campaign_stats_url()
    body = _build_stats_table_write_body()

  elif table == TABLE_CREATIVE:
    key = None
    body = None
  elif table == TABLE_CREATIVE_STATS:
    key = _build_creative_stats_url()
    body = _build_stats_table_write_body()
  else:
    print "Unsupported table name: %s" % table
    return

  url = '%s -d \'%s\'' % (key, body)
  return _build_cluster_url() + url

def _send_query():  
  env = options.env
  router = ROUTER[env]

  if options.tables:
    print ('Supported table names: %s') % (TABLE_NAMES)
  elif options.read:
    url = _build_read_query()
    curli_cmd = 'curli -i %s%s %s' % (router, url, SSH_OPTION)
    print curli_cmd
    result = envRun(curli_cmd)
  elif options.write:
    url = _build_write_query()
    curli_cmd = 'curli -i -X POST %s%s %s' % (router, url, SSH_OPTION)
    print curli_cmd
    result = envRun(curli_cmd)

def envRun(cmd):
  env = options.env
  cmd = cmd
  #if env.startswith('prod-'):
  #  cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  os.system(cmd)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-t', '--table', help='name of the table you want to query.')
  parser.add_option('--tables', action='store_true', dest='tables',  help='list all supported tables.')
  parser.add_option('--acct', help='account id.')
  parser.add_option('--campgroup', help='campaign group id.')
  parser.add_option('--camp', help='campaign id')
  parser.add_option('--crtv', help='creative id')
  parser.add_option('-r', action='store_true', dest='read', help='read table')
  parser.add_option('-w', action='store_true', dest='write', help='write table')
  parser.add_option('--create', action='store_true', dest='create', help='create new entry')
  parser.add_option('-g', '--granu', help='granularity, can be day, lifetime, month')
  parser.add_option('-d', '--day', default=GRANU_DAY_DEFAULT_DAY, help='day, day of the stats entry, if your granularity is lifetime, you do not need this argument.')
  parser.add_option('-b', '--budget', default='100', help='budget in usd, applied when writing espresso table.')
  parser.add_option('--cost', default='100', help='cost in usd, applied when writing espresso table.')
  parser.add_option('--imp', default='1000', help='impression number, applied when writing espresso table.')
  parser.add_option('--click', default='10', help='click number, applied when writing espresso table.')

  parser.add_option('--env', default='ei-ltx1', help='env')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  _send_query()

  print '\n\n'
