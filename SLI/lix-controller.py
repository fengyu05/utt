#!/usr/bin/python
import sys, os, time
import urllib
import json
import ast
import subprocess
import urllib
import base64

options ={}
args = []


CURL = 'curl'

HOME_PATH = os.environ["HOME"]
STORE_PATH = HOME_PATH + '/.lix_ctrl/'

TEE_TMP = STORE_PATH + 'tee'
SID_TMP = STORE_PATH + 'sid'

def infoPrint(msg):
  if not options.mute:
    print msg

def printRun(cmd):
  infoPrint(cmd)
  assert os.system(cmd) == 0

def prepareTmp():
  printRun('mkdir -p %s' % STORE_PATH)

def sidLocate(host):
  return SID_TMP + '.%s' % base64.b64encode(host)

def writeSid(host, sid):
  printRun('echo %s > %s' % (sid, sidLocate(host)))

def cleanSid(host):
  printRun('rm %s' % (sidLocate(host)))

def readSid():
  host=getHost()
  sid = open(sidLocate(host)).read().strip()
  infoPrint('loading sid[%s]' % sid)
  return sid

def teeRun(cmd):
  cmd = cmd + ' | tee %s' % TEE_TMP
  pipeRun(cmd)
  result = open(TEE_TMP).read()

  return result

def envRun(cmd):
  env = options.env
  cmd = cmd
  if env.startswith('prod-'):
    cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', cmd)
  return teeRun(cmd)

def pipeRun(cmd):
  print cmd
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            shell=True)
  output, error = p.communicate()

  if not options.resultOnly:
    print output
    print error
  return output


def makeFabric():
  if options.env:
    return '--fabric=%s' % options.env
  else:
    return ''

def getHost(env='dev'):
  return 'https://lix.corp.linkedin.com/api/v1'

def listArray(input):
  array = json.loads(input)
  for a in array:
    print a


def auth(ldap):
  prepareTmp()
  host = getHost(options.env)
  url = '%s/apiKeys/create' %(host)
  curliCmd = CURL + ' -X POST -H \'Accept: text/plain\' -u %s  \'%s\'' % (ldap, url)
  result = envRun(curliCmd)
  print result
  writeSid(host, result)

def unauth():
  host = getHost(options.env)
  cleanSid(host)

def createTreatmentGroup():
  sid = readSid()
  print sid


def pinotCtrl(args):
  action = args[0]

  ALL_ACTION = {
      'auth': auth,
      'unauth': unauth,
      'createTG': createTreatmentGroup,
      }

  ALL_ACTION[action](*args[1:])


def printHelp():
  print """
  bql.py host query  [--env=prod-lva1]
  """

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='EI3', help='env')
  parser.add_option('-r', '--resultOnly', dest='resultOnly', action='store_true', help='return result only')
  parser.add_option('--mute', dest='mute', default=False, help='mute stdout except return text')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if len(args) < 1:
    printHelp()
    exit(1)

  pinotCtrl(args)

