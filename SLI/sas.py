#!/usr/bin/python
from restli import *
import uuid
import time

# RESOURCE
CREATIVE_RESOURCE = "adCreatives"
CAMPAIGN_RESOURCE = "adCampaigns"
ACCOUNT_RESOURCE = "adAccounts"

# TEST ID on EI

TEST_AD = 100371492
TEST_AD2 = 98710372
TEST_CAMPAIGN = 320033061
TEST_ACCOUNT = 510501414

TEST_CAMPAIGN_FOR_CREATE_CREATIVE = 321589732
TEST_MEMBER = 605

#TEST_SU = 99547902


TEST_SU = 101082032
TEST_CAMPAIGN_FOR_CREATE_CREATIVE_SU = 322404542
TEST_MEMBER_FOR_SU = 60598326
TEST_SU_COMPANY = 62787
TEST_SU_ACCOUNT = 511087488
TEST_SU_ACTIVITY = 5753229212840366080


def genSampleAuditStamps(memberId=TEST_MEMBER):
  timeMillis = int(time.time() * 1000)
  return {
        "created": {
          "actor": "urn:li:member:%s" % memberId,
          "time": timeMillis
          },
        "lastModified": {
          "actor": "urn:li:member:%s" % memberId,
          "time": timeMillis
          }
        }

def genUid():
  return str(uuid.uuid4())

def sendRequest(request):
  request.setEnv(options.env)
  request.execute()

def getTimeRange(startDays, extendDays):
  start = int(time.time() * 1000) + 1000 * 3600 * 24 * startDays
  end = start + 1000 * 3600 * 24 * extendDays 
  return (start, end)

def testCreativeCreate(campaignId=TEST_CAMPAIGN_FOR_CREATE_CREATIVE, memberId=TEST_MEMBER):
  creative = {
      'type' : 'TEXT_AD',
      'parent' : 'urn:li:sponsoredCampaign:%s' % campaignId,
      "variables" : {
        "subType" : {
          "com.linkedin.tscp.TextAdCreativeVariables" : {
            "title" : "creative title",
            "text" : "creative text:" + genUid(),
            "image" : "/AAAAAAAAAAAAAAAAAAAAAAAAxxx.png"
            }
          },
          "href" : "www.google.com"
        },
      "stamps" : genSampleAuditStamps(memberId),
      "review": {
        "reviewStatus": "PENDING"
        },
      "status" : "ACTIVE",
      }

  request = PostRequest(CREATIVE_RESOURCE, 'create', creative)
  request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % memberId)
  sendRequest(request)

def testSUCreate(campaignId=TEST_CAMPAIGN_FOR_CREATE_CREATIVE_SU, memberId=TEST_MEMBER_FOR_SU, activityId=TEST_SU_ACTIVITY):
  creative = {
      'type' : 'SPONSOREDSTATUSUPDATES',
      'parent' : 'urn:li:sponsoredCampaign:%s' % campaignId,
      "reference" : "urn:li:activity:%s" % activityId,
      "variables" : {
        "subType" : {
          "com.linkedin.tscp.SSUCreativeVariables" : {
            }
          },
        },
      "status" : "ACTIVE",
      }

  request = PostRequest(CREATIVE_RESOURCE, 'create', creative)
  request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % memberId)
  sendRequest(request)

def testCreativeCreate2(campaignId=TEST_CAMPAIGN_FOR_CREATE_CREATIVE, memberId=TEST_MEMBER):
  creative = {
      'type' : 'TEXT_AD',
      'parent' : 'urn:li:sponsoredCampaign:%s' % campaignId,
      "variables" : {
        "subType" : {
          "com.linkedin.tscp.TextAdCreativeVariables" : {
            "title" : "creative title",
            "text" : "creative text:" + genUid(),
            "image" : "/AAAAAAAAAAAAAAAAAAAAAAAAxxx.png"
            }
          },
          "href" : "www.google.com"
        },
      "stamps" : genSampleAuditStamps(memberId),
      "status" : "ACTIVE",
      }

  request = PostRequest(CREATIVE_RESOURCE, 'create', creative)
  request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % memberId)
  sendRequest(request)

def testCreativeCreate3(campaignId=TEST_CAMPAIGN_FOR_CREATE_CREATIVE, memberId=TEST_MEMBER):
  creative = {
      'type' : 'TEXT_AD',
      'parent' : 'urn:li:sponsoredCampaign:%s' % campaignId,
      "variables" : {
        "subType" : {
          "com.linkedin.tscp.TextAdCreativeVariables" : {
            "title" : "creative title",
            "text" : "creative text:" + genUid(),
            }
          },
          "href" : "www.google.com"
        },
      "stamps" : genSampleAuditStamps(memberId),
      "status" : "ACTIVE",
      }

  request = PostRequest(CREATIVE_RESOURCE, 'create', creative)
  request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % memberId)
  sendRequest(request)

def testCreateCampaignSU(advertiserId=TEST_MEMBER_FOR_SU, memberId=TEST_MEMBER_FOR_SU):
  timeRange = getTimeRange(10, 90)
  campaign = {
      'parent' : 'urn:li:sponsoredAccount:%s' % advertiserId,
      'name' : 'test campaign SU' + genUid(),
      "type": "SPONSORED_STATUS_UPDATES_V2",
      "runSchedule": {
        "start": timeRange[0],
        "end": timeRange[1]
        },
      "locale": {
        "country": "US",
        "language": "en"
        },
      "targets": {
        "facets": [
          {
            "values": [
              "na.us"
              ],
            "name": "geos"
            },
          {
            "values": [
              "en"
              ],
            "name": "langs"
            }
          ],
        "dataVersion": 4
        },
      "spendLimits": [
        {
          "type": "DAILY",
          "spend": {
            "amount": "100000",
            "currencyCode": "USD"
            }
          }
        ],
      "status": "DRAFT",
      "unitCost": {
        "amount": "2.48",
        "currencyCode": "USD"
        },
      "costType": "CPC",
      "source": "urn:li:multiProduct:tscp-admin-frontend",
      "billingParentReference": "urn:li:finDsm:1232134",
      "servingStatus" : "RUNNABLE",
      "stamps": genSampleAuditStamps()
      }
  request = PostRequest(CAMPAIGN_RESOURCE, 'create', campaign)
  sendRequest(request)

def testCreateCampaign(advertiserId=TEST_ACCOUNT):
  timeRange = getTimeRange(10, 90)
  campaign = {
      'parent' : 'urn:li:sponsoredAccount:%s' % advertiserId,
      'name' : 'test campaign TEXT AD' + genUid(),
      "type": "TEXT_AD",
      "runSchedule": {
        "start": timeRange[0],
        "end": timeRange[1]
        },
      "locale": {
        "country": "US",
        "language": "en"
        },
      "targets": {
        "facets": [
          {
            "values": [
              "na.us"
              ],
            "name": "geos"
            },
          {
            "values": [
              "en"
              ],
            "name": "langs"
            }
          ],
        "dataVersion": 4
        },
      "spendLimits": [
        {
          "type": "DAILY",
          "spend": {
            "amount": "100000",
            "currencyCode": "USD"
            }
          }
        ],
      "status": "ACTIVE",
      "unitCost": {
        "amount": "2.48",
        "currencyCode": "USD"
        },
      "costType": "CPC",
      "source": "urn:li:multiProduct:tscp-admin-frontend",
      "billingParentReference": "urn:li:finDsm:1232134",
      "servingStatus" : "RUNNABLE",
      "stamps": genSampleAuditStamps()
      }

  request = PostRequest(CAMPAIGN_RESOURCE, 'create', campaign)
  sendRequest(request)

def testUpdateCreativeContent(creativeId=TEST_AD, memberId=TEST_MEMBER):
  memberId = 276
  patch = {
      "patch" : {
        "$set": {
          "variables" : {
            "subType" : {
              "com.linkedin.tscp.TextAdCreativeVariables" : {
                "title" : "creative title",
                "text" : "creative text:" + genUid(),
                "image" : "/AAAAAAAAAAAAAAAAAAAAAAAAxxx.png"
                }
              },
              "href" : "www.google.com"
            },
        }
      }
  }

  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % memberId)
  request.addUser('urn:li:member:%s' % memberId)
  request.addPassword('password')
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testUpdateSU(creativeId=TEST_SU):
  patch = {
      "patch" : {
        "$set": {
          "reference" : "urn:li:activity:5770648731661631487",
        }
      }
  }

  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testUpdateCampaignStauts(campaignId, status):
  patch = {
      "patch" : {
        "$set": {
          "status" : status,
        }
      }
  }

  request = PostRequest(CAMPAIGN_RESOURCE, 'partial_update', patch, campaignId)
  sendRequest(request)

  request = GetRequest(CAMPAIGN_RESOURCE, id=campaignId)
  sendRequest(request)

def getCampaignLimit(campaignType="SPONSORED_STATUS_UPDATES_V2"):
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
      "targets":{"dataVersion":4,"facets":[{"values":["na.us"],"name":"geos"},{"values":["en"],"name":"langs"}]}}
  }

  request = ActionRequest(CAMPAIGN_RESOURCE, 'campaignLimits', data)
  sendRequest(request)


def testUpdateCreativeContent2(creativeId=TEST_AD2):
  patch = {
      "patch" : {
        "$set": {
          "variables" : {
            "subType" : {
              "com.linkedin.tscp.TextAdCreativeVariables" : {
                "title" : "creative title",
                "text" : "creative text:" + genUid(),
                "image" : "/AAAAAAAAAAAAAAAAAAAAAAAAxxx.png"
                }
              },
              "href" : "www.google.com"
            },
        }
      }
  }

  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  request.addHeader('Authenticate: X-RestLi urn:li:member:26733270')
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)


def testUpdateCreativeWhole(creativeId=TEST_AD):
  creative = {
      "variables" : {
        "subType" : {
          "com.linkedin.tscp.TextAdCreativeVariables" : {
            "title" : "creative title",
            "text" : "creative text:" + genUid(),
            "image" : "/AAAAAAAAAAAAAAAAAAAAAAAAxxx.png"
            }
          },
          "href" : "www.google.com"
        },
      "stamps" : genSampleAuditStamps(),
      "review": {
        "reviewStatus": "PENDING"
        },
      "status": "ACTIVE",
      "partitionId": 510501414,
      "parent": "urn:li:sponsoredCampaign:320033061",
      "badContent": False,
      "billingReference": "urn:li:finDfp:0",
      "deferredReview": False,
      "id": 99246671,
      "servingStatus": "STOPPED",
      #'contentTimestamp' : 0,
      "type": "TEXT_AD"
    }

  request = PutRequest(CREATIVE_RESOURCE, id=creativeId, data=creative)
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def pauseCreative(creativeId=TEST_AD):
  patch = {
      "patch" : {
        "$set": {
          "status" : "PAUSED"
        }
      }
  }

  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  request.addHeader('Authenticate: X-RestLi urn:li:member:650')
  sendRequest(request)

def testUpdateCreativeReview(creativeId=TEST_AD, Review="APPROVED"):
  patch = {
      "patch" : {
        "$set": {
          "review" : {
            "reviewStatus" : Review
          },
        }
      }
  }
  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  #request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % TEST_MEMBER)
  request.addHeader('Authenticate: X-RestLi SUPERUSER:urn:li:system:0')
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testUpdateCreativeStatus(creativeId=TEST_AD, status="ACTIVE"):
  patch = {
      "patch" : {
        "$set": {
          "status" : status,
        }
      }
  }
  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  #request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % TEST_MEMBER)
  request.addHeader('Authenticate: X-RestLi SUPERUSER:urn:li:system:0')
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def autoApproveCreative(creativeId=TEST_AD):
  patch = {
      "patch" : {
        "$set": {
          "review" : {
            "reviewStatus" : "AUTO_APPROVED"
          },
        }
      }
  }
  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  request.addHeader('Authenticate: X-RestLi SUPERUSER:urn:li:system:0')
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testUpdateCreativeReviewReason(creativeId=TEST_AD):
  patch = {
      "patch" : {
        "$set": {
          "review" : {
            "reviewStatus" : 'REJECTED',
            "rejectionReasons" : [
              { 'reason': 'OFFER_NOT_FOUND'}, { 'reason': 'MISLEADING_CLAIMS'},
              ]
          },
        }
      }
  }
  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  #request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % TEST_MEMBER)
  request.addHeader('Authenticate: X-RestLi SUPERUSER:urn:li:system:0')
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testUpdateCreativeReviewReason2(creativeId=TEST_AD):
  patch = {
      "patch" : {
        "$set": {
          "review" : {
            "reviewStatus" : 'REJECTED',
            "rejectionReasons" : [
              { 'reason': 'OFFER_NOT_FOUND'}, { 'reason': 'DECEPTIVE_BEHAVIOR'},
              ]
          },
        }
      }
  }
  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  #request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % TEST_MEMBER)
  request.addHeader('Authenticate: X-RestLi SUPERUSER:urn:li:system:0')
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testUpdateCreativeReviewReasonOld(creativeId=TEST_AD):
  patch = {
      "patch" : {
        "$set": {
          "review" : {
            "reviewStatus" : 'REJECTED',
            "rejectionCode" : 'BROKEN_URL',
          },
        }
      }
  }
  request = PostRequest(CREATIVE_RESOURCE, 'partial_update', patch, creativeId)
  request.addHeader('Authenticate: X-RestLi urn:li:member:%s' % TEST_MEMBER)
  sendRequest(request)

  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testCreativeDelete(creativeId):
  deleteRequest = DeleteRequest(CREATIVE_RESOURCE, creativeId)
  deleteRequest.execute()


def testGetCreative(creativeId=TEST_AD):
  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testGetSU(creativeId=TEST_SU):
  request = GetRequest(CREATIVE_RESOURCE, id=creativeId)
  sendRequest(request)

def testGetCampaign(campaignId=TEST_CAMPAIGN):
  request = GetRequest(CAMPAIGN_RESOURCE, id=campaignId)
  sendRequest(request)

def testGetAccount(accountId=TEST_ACCOUNT):
  request = GetRequest(ACCOUNT_RESOURCE, id=accountId)
  sendRequest(request)

def testPutCreative(creativeId):
  creative = {
  }
  request = PutRequest(CREATIVE_RESOURCE, id=creativeId, data=creative)
  sendRequest(request)

def testSearchCreative(advertiserId=TEST_ACCOUNT, campaignId=TEST_CAMPAIGN):
  #curli --pretty-print "d2://adCreatives?q=search&facet=partitionId,510501414&facet=parent,urn:li:sponsoredCampaign:320033061"

  facetData = {
    'partitionId' :advertiserId,
    'parent' : 'urn:li:sponsoredCampaign:' + str(campaignId)
  }
  sortData = ['+id']
  request = FacetFinderRequest(CREATIVE_RESOURCE, 'search', facetData, sortData)
  sendRequest(request)

def listCreative():
  facetData = {
      }
  request = FacetFinderRequest(CREATIVE_RESOURCE, 'search', facetData)
  sendRequest(request)

def testSearchNewCreative(advertiserId=TEST_ACCOUNT, campaignId=TEST_CAMPAIGN_FOR_CREATE_CREATIVE):
  #curli --pretty-print "d2://adCreatives?q=search&facet=partitionId,510501414&facet=parent,urn:li:sponsoredCampaign:320033061"

  facetData = {
    'partitionId' :advertiserId,
    'parent' : 'urn:li:sponsoredCampaign:' + str(campaignId)
  }
  sortData = ['+id']
  request = FacetFinderRequest(CREATIVE_RESOURCE, 'search', facetData, sortData)
  sendRequest(request)

def testSearchSUCreative(advertiserId=510501414, campaignId=TEST_CAMPAIGN_FOR_CREATE_CREATIVE_SU):
  #curli --pretty-print "d2://adCreatives?q=search&facet=partitionId,510501414&facet=parent,urn:li:sponsoredCampaign:320033061"

  facetData = {
    'partitionId' :advertiserId,
    'parent' : 'urn:li:sponsoredCampaign:' + str(campaignId)
  }
  sortData = ['+id']
  request = FacetFinderRequest(CREATIVE_RESOURCE, 'search', facetData, sortData)
  sendRequest(request)

def searchActiveSU(campaignId=313686272, fields=['id']):
  #curli 'd2://adCreatives?q=search&facet=parent,urn:li:sponsoredCampaign:313686272&fields=id&facet=status,ACTIVE'

  facetData = {
    'parent' : 'urn:li:sponsoredCampaign:' + str(campaignId),
    'status' : 'ACTIVE',
  }
  request = FacetFinderRequest(CREATIVE_RESOURCE, 'search', facetData)
  request.setFields(fields)
  sendRequest(request)

def pauseAllActiveCreative(campaignId=313686272):
  searchActiveSU(campaignId)


def testSearchCampaign(advertiserId=510501414, count=1):

  facetData = {
      'parent' : 'urn:li:sponsoredAccount:%s' % advertiserId,
  }
  sortData = ['+id']
  pageData = { "count": count, "links": [], "start": 0 }
  request = FacetFinderRequest(CAMPAIGN_RESOURCE, 'search', facetData, sortData, pageData)
  sendRequest(request)

def main(args):

  action = args[0]
  ALL_ACTION = {
#CREATIVE
      'getCreative' : testGetCreative,
      'getSU' : testGetSU,
      'createCreative': testCreativeCreate,
      'createCreative2': testCreativeCreate2,
      'createCreative3': testCreativeCreate3,
      'createSU': testSUCreate,
      'updateCreativeStatus': testUpdateCreativeStatus,
      'updateCreativeContent': testUpdateCreativeContent,
      'updateSU': testUpdateSU,
      'updateCreativeContent2': testUpdateCreativeContent2,
      'updateCreativeWhole': testUpdateCreativeWhole,
      'updateCreativeReview': testUpdateCreativeReview,
      'autoApproveCreative': autoApproveCreative,
      'updateCreativeReviewReason': testUpdateCreativeReviewReason,
      'updateCreativeReviewReason2': testUpdateCreativeReviewReason2,
      'searchCreative': testSearchCreative,
      'listCreative': listCreative,
      'searchNewCreative': testSearchNewCreative,
      'searchSUCreative': testSearchSUCreative,
      'pauseCreative': pauseCreative,
      'searchActiveSU': searchActiveSU,
      'pauseAllActiveCreative': pauseAllActiveCreative,

#CAMPAIGN
      'getCampaign' : testGetCampaign,
      'createCampaign' : testCreateCampaign,
      'createSUCampaign' : testCreateCampaignSU,
      'searchCampaign': testSearchCampaign,
      'updateCampaignStatus': testUpdateCampaignStauts,
      'getCampaignLimit' : getCampaignLimit,

#ACCOUNT
      'getAccount' : testGetAccount,
      'getAdvertiser' : testGetAccount,


  }

  if action in ALL_ACTION:
    ALL_ACTION[action](*args[1:])

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='', help='env')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if (len(args) < 1):
    parser.print_help()
    exit()

  main(args)
