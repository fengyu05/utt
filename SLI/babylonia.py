#!/usr/bin/python
from restli import *
import uuid
import time
import urllib

# RESOURCE
INGESTION_RESOURCE= "contentIngestionTasks"
SUMMARY_SOURCE= "ingestedContentSummaries"


def genUid():
  return str(uuid.uuid4())


def extractOnly(url):
  request = PutRequest(INGESTION_RESOURCE, urlParam={ 'url': url, 'config.reason' : 'EXTRACT_ONLY' })
  request.execute()

def share(url):
  request = PutRequest(INGESTION_RESOURCE, urlParam={ 'url': url, 'config.reason' : 'SHARE' })
  request.execute()

def getIngestion(url):
  request = GetRequest(INGESTION_RESOURCE, urlParam={ 'url': url, 'config.reason' : 'EXTRACT_ONLY' })
  request.execute()

def getShare(url):
  request = GetRequest(INGESTION_RESOURCE, urlParam={ 'url': url, 'config.reason' : 'SHARE' })
  request.execute()

def getSummary(id):
  request = GetRequest(SUMMARY_SOURCE, id)
  request.execute()

def main(args):

  action = args[0]
  ALL_ACTION = {
      'extract' : extractOnly,
      'share' : share,
      'get' : getIngestion,
      'getShare' : getShare,

      'sum' : getSummary,
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
