#!/usr/bin/python
"""
Copy file from gateway
"""
__author__ = 'zhdeng'

import sys, os, time, datetime, glob, uuid, io, random, getpass


REMOTE_FILE_CACHE_PATH = '~/.copy_from_gateway_file_cache'

options = dict()

ENV_HOLDEM = 'holdem'
ENV_CANASTA = 'canasta'
ENV_WAR = 'war'
ENV_NERTZ = 'nertz'

HOST = {
  ENV_HOLDEM: 'ltx1-holdemgw01.grid.linkedin.com',
  ENV_CANASTA: 'eat1-canastagw01.grid.linkedin.com',
  ENV_NERTZ: 'eat1-nertzgw01.grid.linkedin.com',
  ENV_WAR: 'lva1-wargw01.grid.linkedin.com',
}

DEFAULT_OUTPATH = os.environ['HOME'] + '/incoming'

def printRun(cmd):
  print cmd
  assert os.system(cmd) == 0


def copyFromGateway(inputFolder, env):
  if env not in HOST:
    print 'Noknown host env  %s' % env
    exit(1)
  host = HOST[env]
  username = getpass.getuser()
  target = options.outputPath

  if inputFolder[-1] == '/':
    inputFolder = inputFolder[:-1]
  basename = os.path.basename(inputFolder)
  assert basename, 'terget basename is empty'
  rmCmd = 'rm -rf %s' % (target + '/' + basename)
  printRun(rmCmd)
  cmd1 = 'ssh -q -K -tt %s "rm -rf %s;mkdir %s;hadoop fs -copyToLocal %s %s/"' % (host, REMOTE_FILE_CACHE_PATH, REMOTE_FILE_CACHE_PATH, inputFolder, REMOTE_FILE_CACHE_PATH)
  printRun(cmd1)
  renameTarget = target + '/' + basename
  printRun('mkdir -p %s' % renameTarget)
  cmd2 = 'scp -r %s@%s:%s/%s/* %s' % (username, host, REMOTE_FILE_CACHE_PATH, basename, renameTarget)
  printRun(cmd2)
  return renameTarget


def ensureDir(dirName):
  """
  Create directory if necessary.
  """
  if not os.path.exists(dirName):
    os.makedirs(dirName)


def main(args):
  ensureDir(options.outputPath)
  for arg in args:
    result = copyFromGateway(arg, options.env)
    print 'copy file in %s' % result

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
