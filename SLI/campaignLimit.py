#!/usr/bin/python
from restli import *
import random
import uuid
import time

options = {}

# RESOURCE
CREATIVE_RESOURCE = "adCreatives"
CAMPAIGN_RESOURCE = "adCampaigns"
ACCOUNT_RESOURCE = "adAccounts"

CAMPAIGN_TYPES = ["SPONSORED_STATUS_UPDATES_V2", "TEXT_AD"]

GEOS = [
"af",
"af.eg",
"af.za",
"aq",
"as",
"as.cn",
"as.hk",
"as.in",
"as.in.an",
"as.in.ap",
"as.in.ap.6508",
"as.in.ar",
"as.in.as",
"as.in.br",
"as.in.ch",
"as.in.cg",
"as.in.dn",
"as.in.dd",
"as.in.dl",
"as.in.dl.7151",
"as.in.ga",
"as.in.gj",
"as.in.gj.7065",
"as.in.gj.6552",
"as.in.hr",
"as.in.hr.7391",
"as.in.hp",
"as.in.jk",
"as.in.jh",
"as.in.ka",
"as.in.ka.7127",
"as.in.kl",
"as.in.kl.6477",
"as.in.ld",
"as.in.mp",
"as.in.mp.7382",
"as.in.mh",
"as.in.mh.7150",
"as.in.mh.6751",
"as.in.mh.7350",
"as.in.mn",
"as.in.ml",
"as.in.mz",
"as.in.nl",
"as.in.or",
"as.in.py",
"as.in.pb",
"as.in.pb.6879",
"as.in.rj",
"as.in.rj.7287",
"as.in.sk",
"as.in.tn",
"as.in.tn.6891",
"as.in.tn.6472",
"as.in.tr",
"as.in.up",
"as.in.up.7093",
"as.in.up.7392",
"as.in.ul",
"as.in.wb",
"as.in.wb.7003",
"as.id",
"as.jp",
"as.my",
"as.ph",
"as.sg",
"as.th",
"eu",
"eu.be",
"eu.bg",
"eu.hr",
"eu.cz",
"eu.dk",
"eu.dk.*.5038",
"eu.dk.*.5041",
"eu.dk.*.5044",
"eu.dk.*.5045",
"eu.fi",
"eu.fr",
"eu.fr.*.5205",
"eu.fr.*.5210",
"eu.fr.*.5211",
"eu.fr.*.5221",
"eu.fr.*.5227",
"eu.fr.*.5249",
"eu.de",
"eu.gr",
"eu.hu",
"eu.ie",
"eu.it",
"eu.it.*.5587",
"eu.it.*.5616",
"eu.it.*.5636",
"eu.it.*.5652",
"eu.it.*.5657",
"eu.nl",
"eu.nl.*.5663",
"eu.nl.*.5664",
"eu.nl.*.5665",
"eu.nl.*.5906",
"eu.nl.*.5668",
"eu.nl.*.5669",
"eu.nl.*.5673",
"eu.nl.*.7417",
"eu.nl.*.5681",
"eu.nl.*.5908",
"eu.nl.*.5688",
"eu.nl.*.5907",
"eu.nl.*.5690",
"eu.no",
"eu.pl",
"eu.pt",
"eu.ro",
"eu.ru",
"eu.es",
"eu.se",
"eu.ch",
"eu.tr",
"eu.ua",
"eu.gb",
"eu.gb.*.4544",
"eu.gb.*.4550",
"eu.gb.*.4552",
"eu.gb.*.4555",
"eu.gb.*.4558",
"eu.gb.*.4562",
"eu.gb.*.4574",
"eu.gb.*.4579",
"eu.gb.*.4580",
"eu.gb.*.4582",
"eu.gb.*.4583",
"eu.gb.*.4586",
"eu.gb.*.4597",
"eu.gb.*.4606",
"eu.gb.*.4603",
"eu.gb.*.4573",
"eu.gb.*.4608",
"eu.gb.*.4610",
"eu.gb.*.4612",
"eu.gb.*.4613",
"eu.gb.*.4618",
"eu.gb.*.4623",
"eu.gb.*.4625",
"eu.gb.*.4626",
"eu.gb.*.4628",
"eu.gb.*.4632",
"eu.gb.*.4635",
"eu.gb.*.4644",
"eu.gb.*.4648",
"la",
"la.ar",
"la.br",
"la.br.ac",
"la.br.al",
"la.br.ap",
"la.br.am",
"la.br.ba",
"la.br.ce",
"la.br.df",
"la.br.es",
"la.br.go",
"la.br.ma",
"la.br.mt",
"la.br.ms",
"la.br.mg",
"la.br.mg.6156",
"la.br.pr",
"la.br.pr.6399",
"la.br.pb",
"la.br.pa",
"la.br.pe",
"la.br.pi",
"la.br.rn",
"la.br.rs",
"la.br.rs.6467",
"la.br.rj",
"la.br.rj.6034",
"la.br.ro",
"la.br.rr",
"la.br.sc",
"la.br.se",
"la.br.sp",
"la.br.sp.6104",
"la.br.sp.6368",
"la.br.to",
"la.cl",
"la.mx",
"me",
"me.bh",
"me.il",
"me.jo",
"me.kw",
"me.pk",
"me.qa",
"me.sa",
"me.ae",
"na",
"na.ca",
"na.ca.ab",
"na.ca.ab.4882",
"na.ca.ab.4872",
"na.ca.bc",
"na.ca.bc.4873",
"na.ca.bc.4880",
"na.ca.mb",
"na.ca.nb",
"na.ca.nl",
"na.ca.nt",
"na.ca.ns",
"na.ca.nu",
"na.ca.on",
"na.ca.on.4865",
"na.ca.on.4869",
"na.ca.on.4864",
"na.ca.on.4884",
"na.ca.on.4876",
"na.ca.pe",
"na.ca.qc",
"na.ca.qc.4863",
"na.ca.qc.4875",
"na.ca.sk",
"na.ca.yt",
"na.us",
"na.us.al",
"na.us.al.100",
"na.us.al.344",
"na.us.al.516",
"na.us.ak",
"na.us.ak.38",
"na.us.az",
"na.us.az.620",
"na.us.az.852",
"na.us.ar",
"na.us.ar.258",
"na.us.ar.440",
"na.us.ca",
"na.us.ca.284",
"na.us.ca.49",
"na.us.ca.732",
"na.us.ca.51",
"na.us.ca.82",
"na.us.ca.712",
"na.us.ca.84",
"na.us.ca.748",
"na.us.ca.812",
"na.us.co",
"na.us.co.172",
"na.us.co.267",
"na.us.co.34",
"na.us.ct",
"na.us.ct.327",
"na.us.ct.552",
"na.us.de",
"na.us.dc",
"na.us.fl",
"na.us.fl.202",
"na.us.fl.270",
"na.us.fl.271",
"na.us.fl.290",
"na.us.fl.359",
"na.us.fl.398",
"na.us.fl.490",
"na.us.fl.56",
"na.us.fl.596",
"na.us.fl.751",
"na.us.fl.824",
"na.us.fl.828",
"na.us.fl.896",
"na.us.ga",
"na.us.ga.60",
"na.us.ga.52",
"na.us.ga.752",
"na.us.hi",
"na.us.hi.332",
"na.us.id",
"na.us.id.108",
"na.us.il",
"na.us.il.14",
"na.us.il.612",
"na.us.il.688",
"na.us.il.140",
"na.us.in",
"na.us.in.244",
"na.us.in.276",
"na.us.ia.348",
"na.us.ia",
"na.us.ia.196",
"na.us.ia.212",
"na.us.ks",
"na.us.ks.904",
"na.us.ky",
"na.us.ky.428",
"na.us.ky.452",
"na.us.la",
"na.us.la.76",
"na.us.la.556",
"na.us.me",
"na.us.me.640",
"na.us.md",
"na.us.md.7416",
"na.us.ma",
"na.us.ma.7",
"na.us.ma.800",
"na.us.mi",
"na.us.mi.35",
"na.us.mi.300",
"na.us.mi.372",
"na.us.mi.404",
"na.us.mi.696",
"na.us.mn",
"na.us.mn.512",
"na.us.ms",
"na.us.ms.356",
"na.us.mo",
"na.us.mo.174",
"na.us.mo.704",
"na.us.mo.376",
"na.us.mo.792",
"na.us.mt",
"na.us.ne",
"na.us.ne.592",
"na.us.ne.436",
"na.us.nv",
"na.us.nv.412",
"na.us.nv.672",
"na.us.nh",
"na.us.nj",
"na.us.nm",
"na.us.nm.20",
"na.us.ny",
"na.us.ny.16",
"na.us.ny.128",
"na.us.ny.70",
"na.us.ny.96",
"na.us.ny.684",
"na.us.ny.816",
"na.us.nc",
"na.us.nc.48",
"na.us.nc.152",
"na.us.nc.312",
"na.us.nc.664",
"na.us.nc.920",
"na.us.nd",
"na.us.oh",
"na.us.oh.21",
"na.us.oh.28",
"na.us.oh.184",
"na.us.oh.200",
"na.us.oh.840",
"na.us.ok",
"na.us.ok.588",
"na.us.ok.856",
"na.us.or",
"na.us.or.240",
"na.us.or.79",
"na.us.pa",
"na.us.pa.24",
"na.us.pa.77",
"na.us.pa.628",
"na.us.pa.324",
"na.us.pa.400",
"na.us.pa.756",
"na.us.ri",
"na.us.ri.648",
"na.us.sc",
"na.us.sc.144",
"na.us.sc.176",
"na.us.sc.316",
"na.us.sd",
"na.us.sd.776",
"na.us.tn",
"na.us.tn.156",
"na.us.tn.492",
"na.us.tn.536",
"na.us.tn.366",
"na.us.tn.384",
"na.us.tx",
"na.us.tx.64",
"na.us.tx.31",
"na.us.tx.232",
"na.us.tx.42",
"na.us.tx.724",
"na.us.ut",
"na.us.ut.716",
"na.us.ut.652",
"na.us.vt",
"na.us.vt.130",
"na.us.va",
"na.us.va.154",
"na.us.va.572",
"na.us.va.676",
"na.us.va.680",
"na.us.wa",
"na.us.wa.91",
"na.us.wa.784",
"na.us.wv",
"na.us.wi",
"na.us.wi.63",
"na.us.wi.308",
"na.us.wi.472",
"na.us.wi.46",
"na.us.wy",
"oc",
"oc.au",
"oc.au.*.4886",
"oc.au.*.4909",
"oc.au.*.4893",
"oc.au.*.4900",
"oc.au.*.4905",
"oc.au.*.4910",
"oc.nz"
]

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

def getCampaignLimit(campaignType="SPONSORED_STATUS_UPDATES_V2", geo="na.us", targets=''):
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
      "costType":"CPC",
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

  request = ActionRequest(CAMPAIGN_RESOURCE, 'campaignLimits', data)
  if options.host:
    request.setLocalResource("http://%s/sas-campaign/resources/adCampaigns" % options.host)
  elif options.local:
    request.setLocalResource("http://localhost:%s/sas-campaign/resources/adCampaigns" % options.port)

  if options.concurrent:
    request.setConcurrent(True)

  request.setEnv(options.env)
  request.execute()

def ramdomBidSuggestInUs():
  getCampaignLimit(random.choice(CAMPAIGN_TYPES), random.choice(GEOS))

def testCampaignLimits():
  getCampaignLimit(options.campaignType, '', options.targets)

def testMemberFloor():
  getCampaignLimit('SPONSORED_STATUS_UPDATES_V2', random.choice(['la.br', 'as.in']))

def testInmailFloor():
  getCampaignLimit('SPONSORED_INMAILS', random.choice(GEOS))

def main(args):

  if (len(args) > 0 and args[0] == 'load_bs'):
    setattr(options, 'concurrent', True)
    while True:
      ramdomBidSuggestInUs()
      time.sleep(options.time)
  elif len(args) > 0 and args[0] == 'memberFloor':
    testMemberFloor()
  elif len(args) > 0 and args[0] == 'im':
    testInmailFloor()
  elif len(args) > 0 and args[0] == 'cl':
    testCampaignLimits()
  else:
    ramdomBidSuggestInUs()


if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='', help='env')
  parser.add_option('-t', '--time', type=float, default=1.0, help='sleep time')
  parser.add_option('-l', '--local', action="store_true", help='localhost')
  parser.add_option('--host', default="", help='host name')
  parser.add_option('-p', '--port', default=9999, help='port')
  parser.add_option('--ct', dest='campaignType', default='SPONSORED_STATUS_UPDATES_V2', help='campaignType')
  parser.add_option('--targets', dest='targets', default='', help='targets')
  parser.add_option('--concurrent', action="store_true")

  global options
  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  main(args)
