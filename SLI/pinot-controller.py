#!/usr/bin/python
import sys, os, time
import urllib
import json
import ast
import subprocess
import urllib

options ={}
args = []

HOST = {
    'EI3' : 'http://ei3-pinot-controller.stg.linkedin.com:11984',
    'ei-lca1' : 'http://lca1-pinot-controller.stg.linkedin.com:11984',
    'ei-ltx1' : 'http://ltx1-pinot-controller.stg.linkedin.com:11984',

    'prod-lva1' :'http://lva1-app8554.prod.linkedin.com:11984',
}
'''
---- Fabric prod-lva1 ----
pinot-controller lva1-app8554.prod.linkedin.com  i001  0.1.367 15511                                            ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
pinot-controller lva1-app8632.prod.linkedin.com  i001  0.1.367 15511                                            ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
pinot-controller lva1-app8707.prod.linkedin.com  i001  0.1.367 15511                                            ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
---- Fabric prod-ltx1 ----
pinot-controller ltx1-app9816.prod.linkedin.com  i001  0.1.367 15511                                            ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
pinot-controller ltx1-app9841.prod.linkedin.com  i001  0.1.367 15511                                            ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
pinot-controller ltx1-app9968.prod.linkedin.com  i001  0.1.367 15511                                            ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
---- Fabric prod-lsg1 ----
pinot-controller lsg1-app0166.prod.linkedin.com i001  0.1.367 15511   ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
pinot-controller lsg1-app0199.prod.linkedin.com i001  0.1.367 15511   ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
pinot-controller lsg1-app0200.prod.linkedin.com i001  0.1.367 15511   ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
pinot-controller lsg1-app0201.prod.linkedin.com i001  0.1.367 15511   ca753078ebc2c3a89d1891fe6b3957d4ee3dc117 
---- Fabric prod-lor1 ----
pinot-controller lor1-app1689.prod.linkedin.com i001  0.1.367 15511                        5b52ec61-bbed-4e9a-aeb9-01046fa6ba01 
pinot-controller lor1-app1773.prod.linkedin.com i001  0.1.367 15511                        5b52ec61-bbed-4e9a-aeb9-01046fa6ba01 
pinot-controller lor1-app1942.prod.linkedin.com i001  0.1.367 15511                        5b52ec61-bbed-4e9a-aeb9-01046fa6ba01 
'''


TEE_TMP = '/tmp/tee.pinotCtrl'
CURL = 'curl'

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

def getPinotHost(env):
  return HOST[env]

def listArray(input):
  array = json.loads(input)
  for a in array:
    print a

def listSegments(table):
  host = getPinotHost(options.env)
  url = '%s/segments/%s' % (host, table)
  curliCmd = CURL + ' -s -X GET --header \'Accept: text/plain\' \'%s\'' % (url)
  result = envRun(curliCmd)

  listArray(result)

def deleteSegment(table, segment):
  host = getPinotHost(options.env)
  url = '%s/segments/%s/%s' % (host, table, segment)
  curliCmd = CURL + ' -X DELETE --header \'Accept: text/plain\' \'%s\'' % (url)
  result = envRun(curliCmd)
  print result

def showUI():
  host = getPinotHost(options.env)
  url = '%s/swagger-ui/index.html?url=/api' % (host)
  print url

def pinotCtrl(args):
  action = args[0]

  ALL_ACTION = {
      'segments': listSegments,
      'delete_segment': deleteSegment,
      'ui' : showUI,
      }

  ALL_ACTION[action](*args[1:])


def printHelp():
  print """
  bql.py host query  [--env=prod-lva1]
  """

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='ei-lca1', help='env')
  parser.add_option('-r', '--resultOnly', dest='resultOnly', action='store_true', help='return result only')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if len(args) < 1:
    printHelp()
    exit(1)

  pinotCtrl(args)

