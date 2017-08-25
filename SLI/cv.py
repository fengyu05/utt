#!/usr/bin/python
from restli import *
import os
import uuid
import time

# RESOURCE
UCV_RESOURCE = "contentClassification"
CRC_RESOURCE = "lowQualityClassifiers"
BAM_RESORUCE = "classifySpam"

def makeAdClassficationContentInfo(title, text, url, creativeId, companyId):
  return {
      "sponsoredCreativeUrn" : "urn:li:sponsoredCreative:%d" % creativeId,
      "title" : "",
      "description" : "",
      "commentary" : "",
      "externalReferenceHref" : { 'com.linkedin.common.Uri' :url},
      "externalReferenceTitle" : title,
      "externalReferenceDescription" : text,
      "externalReferenceEntity" : "urn:li:company:%d" % companyId
  }

def makeCreativeVariables(title, text, url):
  return {
      "href": url,
      "subType" : {
        "com.linkedin.tscp.TextAdCreativeVariables": {
          "title": title,
          "text" : text,
        }
      }
    }

def classifySU(title='title', text='text', url='www.linkedin.com', creativeId=99246771, memberId=362025):
  data = {
      "batchClassificationRequest" : {
        "classificationRequests" : [
          {
            "contentData": {
              "contentText": {
                "AdClassificationContentInfo": makeAdClassficationContentInfo(title, text, url, creativeId, 1),
              },
            },
            "contentSource": "SAS_SPONSORED_UPDATE",
            "content" : "urn:li:sponsoredCreative:%d" % creativeId,
            "creationContext" : {
              "memberSession": "urn:li:memberSession:(urn:li:member:%d,36676301)" % memberId,
              "contentCreator" : "urn:li:member:%d" % memberId,
              "lastModificationTime" : long(time.time() * 1000),
              },
            "trackingId" : str(uuid.uuid4())[:16],
            }
          ],
          "trackingId" : str(uuid.uuid4()),
        },
      "isSynchronous" : not options.async,
  }
  request = ActionRequest(UCV_RESOURCE, 'classifyContent', data)

  if options.local:
    request.setLocalResource("http://localhost:%s/ucv/%s" % (options.port,UCV_RESOURCE))
  request.setEnv(options.env)
  request.execute()

def classifyTextAd(title='title', text='text', url='www.linkedin.com', creativeId=99246771, memberId=362025):
  data = {
      "batchClassificationRequest" : {
        "classificationRequests" : [
          {
            "contentData": {
              "contentText": {
                "com.linkedin.tscp.CreativeVariables": makeCreativeVariables(title, text, url),
              },
            },
            "contentSource": "SAS_ADS_CREATIVE",
            "content" : "urn:li:sponsoredCreative:%d" % creativeId,
            "creationContext" : {
              "memberSession": "urn:li:memberSession:(urn:li:member:%d,36676301)" % memberId,
              "lastModificationTime" : long(time.time() * 1000),
              "contentCreator" : "urn:li:member:%d" % memberId,
              },
            "trackingId" : str(uuid.uuid4())[:16],
            },
          ],
          "trackingId" : str(uuid.uuid4()),
        },
      "isSynchronous" : not options.async,
  }
  print data
  request = ActionRequest(UCV_RESOURCE, 'classifyContent', data)

  if options.local:
    request.setLocalResource("http://%s:%s/ucv/%s" % (options.host, options.port,UCV_RESOURCE))
  request.setEnv(options.env)
  request.execute()

def crcClassifySu(title='title', text='text', url='www.linkedin.com', creativeId=99246771, memberId=362025):
  data = {
      "classificationRequests" : {
        "classificationRequests" : [
          {
            "contentData": {
              "contentText": {
                "AdClassificationContentInfo": makeAdClassficationContentInfo(title, text, url, creativeId, 1),
              },
            },
            "contentSource": "SAS_SPONSORED_UPDATE",
            "content" : "urn:li:sponsoredCreative:%d" % creativeId,
            "creationContext" : {
              "memberSession": "urn:li:memberSession:(urn:li:member:%d,36676301)" % memberId,
              "lastModificationTime" : long(time.time() * 1000),
              "contentCreator" : "urn:li:member:%d" % memberId,
              }
            }
          ],
          "trackingId" : str(uuid.uuid4()),
        },
  }
  print data
  request = ActionRequest(CRC_RESOURCE, 'classifyLowQuality', data)
  request.setEnv(options.env)
  request.execute()

def crcClassifyTextAd(title='title', text='text', url='www.linkedin.com', creativeId=99246771, memberId=362025):
  data = {
      "classificationRequests" : {
        "classificationRequests" : [
          {
            "contentData": {
              "contentText": {
                "com.linkedin.tscp.CreativeVariables": makeCreativeVariables(title, text, url),
                }
            },
            "contentSource": "SAS_ADS_CREATIVE",
            "content" : "urn:li:sponsoredCreative:%d" % creativeId,
            "creationContext" : {
              "memberSession": "urn:li:memberSession:(urn:li:member:%d,36676301)" % memberId,
              "lastModificationTime" : long(time.time() * 1000),
              "contentCreator" : "urn:li:member:%d" % memberId,
              }
            }
          ],
          "trackingId" : str(uuid.uuid4()),
        },
  }
  print data
  request = ActionRequest(CRC_RESOURCE, 'classifyLowQuality', data)
  request.setEnv(options.env)
  request.execute()

def bamClassifySu(title='title', text='text', url='www.linkedin.com', creativeId=99246771, memberId=362025):
  data = {
      "batchClassificationRequest" : {
        "classificationRequests" : [
          {
            "contentData": {
              "contentText": {
                "AdClassificationContentInfo": makeAdClassficationContentInfo(title, text, url, creativeId, 1),
              },
            },
            "contentSource": "SAS_SPONSORED_UPDATE",
            "content" : "urn:li:sponsoredCreative:%d" % creativeId,
            "creationContext" : {
              "memberSession": "urn:li:memberSession:(urn:li:member:%d,36676301)" % memberId,
              "lastModificationTime" : long(time.time() * 1000),
              "contentCreator" : "urn:li:member:%d" % memberId,
              },
            "trackingId" : str(uuid.uuid4())[:16]
            }
          ],
          "trackingId" : str(uuid.uuid4()),
        },
      "isSynchronous" : not options.async,
  }
  print data
  request = ActionRequest(BAM_RESORUCE, 'classifySpam', data)
  request.setEnv(options.env)
  request.execute()

def bamClassifyTextAd(title='title', text='text', url='www.linkedin.com', creativeId=99246771, memberId=362025):
  data = {
      "batchClassificationRequest" : {
        "classificationRequests" : [
          {
            "contentData": {
              "contentText": {
                "com.linkedin.tscp.CreativeVariables": makeCreativeVariables(title, text, url),
                }
            },
            "contentSource": "SAS_ADS_CREATIVE",
            "content" : "urn:li:sponsoredCreative:%d" % creativeId,
            "creationContext" : {
              "memberSession": "urn:li:memberSession:(urn:li:member:%d,36676301)" % memberId,
              "lastModificationTime" : long(time.time() * 1000),
              "contentCreator" : "urn:li:member:%d" % memberId,
              },
            "trackingId" : str(uuid.uuid4())[:16]
            },
          ],
          "trackingId" : str(uuid.uuid4()),
        },
      "isSynchronous" : not options.async,
  }
  print data
  request = ActionRequest(BAM_RESORUCE, 'classifySpam', data)
  request.setEnv(options.env)
  request.execute()

def main(args):

  action = args[0]
  ALL_ACTION = {
#CREATIVE
      'su' : classifySU,
      'text' : classifyTextAd,
      'crc_text' : crcClassifyTextAd,
      'crc_su' : crcClassifySu,
      'bam_text' : bamClassifyTextAd,
      'bam_su' : bamClassifySu,
  }

  if action in ALL_ACTION:
    ALL_ACTION[action](*args[1:])

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='', help='env')
  parser.add_option('-l', '--local', action="store_true", help='localhost')
  parser.add_option('-a', '--async', action="store_true", help='async')
  parser.add_option('-m', '--memberId', default="", help='memberId')
  parser.add_option('--host', default="", help='host name')
  parser.add_option('-p', '--port', default=10270, help='port')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if (len(args) < 1):
    parser.print_help()
    exit()

  main(args)
