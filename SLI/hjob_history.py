#!/usr/bin/python
import os
options = {}
args = []

ENV_DEV = 'dev'
ENV_PROD = 'prod'

JH_HOST = {
    ENV_DEV: 'http://eat1-nertzjh01.grid.linkedin.com:19888',
    ENV_PROD: 'http://eat1-nertzjh01.grid.linkedin.com:19888',
    }

RM_HOST = {
    ENV_DEV: 'http://eat1-nertzrm01.grid.linkedin.com:8088',
    ENV_PROD: 'http://eat1-nertzrm01.grid.linkedin.com:8088',
    }

def printRun(cmd):
  print cmd
  assert os.system(cmd) == 0

def getJobHistoryHost(env):
  return JH_HOST[env]

def getResourceManagerHost(env):
  return RM_HOST[env]

def getJobHistory(id):
  url = getJobHistoryHost(options.env) + '/jobhistory/job/job_%s' % id
  print url
  #cmd = 'xdg-open %s &' % url
  #printRun(cmd)


def getAppInRm(id):
  url = getResourceManagerHost(options.env) + '/cluster/app/application_%s' % id
  print url


def main(args):
  action = args[0]
  ALL_ACTION = {
      'jh' : getJobHistory,
      'rm' : getAppInRm,
      }
  if action in ALL_ACTION:
    ALL_ACTION[action](*args[1:])
  else:
    print 'action %s not found' % action
    exit(1)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default=ENV_DEV, help='env')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if (len(args) < 1):
    parser.print_help()
    exit()

  main(args)
