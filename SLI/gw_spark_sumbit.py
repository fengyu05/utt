#!/usr/bin/python
"""
Subit spark job to gateway
"""
__author__ = 'zhdeng'

import sys, os, time, datetime, glob, uuid, io, random, getpass


REMOTE_FILE_CACHE_PATH = '~/.gw_spark_cache'

options = dict()

ENV_HOLDEM = 'holdem'
ENV_WAR = 'war'

HOST = {
  ENV_HOLDEM: 'ltx1-holdemgw01.grid.linkedin.com',
  ENV_WAR: 'lva1-wargw01.grid.linkedin.com',
}

DEFAULT_OUTPATH = os.environ['HOME'] + '/incoming'

def printRun(cmd):
  print cmd
  assert os.system(cmd) == 0


def gwSpark(script):
  env = options.env
  if env not in HOST:
    print 'Noknown host env  %s' % env
    exit(1)
  host = HOST[env]

  username = getpass.getuser()

  cmd0 = 'ssh -q -K -tt %s "rm -rf %s;mkdir %s"' % (host, REMOTE_FILE_CACHE_PATH, REMOTE_FILE_CACHE_PATH)
  cmd1 = 'scp -r %s %s@%s:%s/' % (script, username, host, REMOTE_FILE_CACHE_PATH)

  printRun(cmd0)
  printRun(cmd1)

def ensureDir(dirName):
  """
  Create directory if necessary.
  """
  if not os.path.exists(dirName):
    os.makedirs(dirName)


def main(args):
  ensureDir(options.outputPath)
  gwSpark(*args)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()

  parser.add_option('-o', '--out', dest='outputPath', default=DEFAULT_OUTPATH, help='Output folder')
  parser.add_option('--env', dest='env', default=ENV_HOLDEM, help='Env')

  (options,args) = parser.parse_args()
  if (len(args) == 0):
    parser.print_help()
    exit()

  main(args)
