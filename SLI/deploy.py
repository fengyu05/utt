#!/usr/bin/python
# -- zhdeng --
import os

options = {}
args = []

WAR_KEY = 'war'
TARGET_KEY = 'target'

WARLIST = {
    'insights' : {
        WAR_KEY : 'tscp-insights-war',
        TARGET_KEY : ':tscp-insights-war',
      },
    'campaign' : {
        WAR_KEY : 'tscp-admin-core-war',
        TARGET_KEY : 'tscp-admin-core-war',
      },
    'admin' : {
        WAR_KEY : 'tscp-admin-core-war',
        TARGET_KEY : 'tscp-admin-core-war',
      },
    'proc' : {
       WAR_KEY : 'sasbe-sasproc-war',
       TARGET_KEY : ':sasbe:sasbe-sasproc-war'
      },
    'cspserving' : {
       WAR_KEY : 'sasbe-cspserving-war',
       TARGET_KEY : ':sasbe:sasbe-cspserving-war',
      },
    'targeting' : {
       WAR_KEY : 'tscp-targeting-war',
       TARGET_KEY : 'targeting:tscp-targeting-war',
      },
    'forecast' : {
        WAR_KEY : 'tscp-forecast-war',
        TARGET_KEY : 'tscp-forecast-war',
      },
    'dog' : {
        WAR_KEY : 'watchdog-war',
        TARGET_KEY : 'watchdog-war',
      },
    'cv' : {
      WAR_KEY : 'content-validation-war',
      TARGET_KEY : 'content-validation:content-validation-war',
      },
    'crc' : {
      WAR_KEY : 'content-relevance-classifiers-server-war',
      TARGET_KEY : 'content-relevance-classifiers-server-war',
      },
    'jmr-forecast' : {
      WAR_KEY : 'jobs-marketplace-forecasting-restli-war',
      TARGET_KEY : 'jobs-marketplace-forecasting-restli-war',
      },
    'jobforecast' : {
      WAR_KEY : 'jobs-marketplace-forecasting-restli-war',
      TARGET_KEY : 'jobs-marketplace-forecasting-restli-war',
      },
    }

def printRun(cmd):
  print cmd
  if not options.skipAssert:
    assert os.system(cmd) == 0
  else:
    os.system(cmd)


def main(args):
  war = args[0]
  if war not in WARLIST:
    print 'WAR key %s not register' % war
    exit(1)

  warName = WARLIST[war][WAR_KEY]
  target = WARLIST[war][TARGET_KEY]

  if not options.redeploy:
    if not options.skipClean:
      printRun('mint clean') #= printRun('mint kill'), printRun('mint clean-containers')

    printRun('ligradle %s:build' % target)

    if not options.skipCfg:
      printRun('mint build-cfg -w %s -f %s' % (warName, options.env))
      printRun('mint release-cfg')

  debugFlag = '--debug-app'
  if options.skipDebug:
    debugFlag = ''
  printRun('mint deploy -w %s -f %s %s' % (warName, options.env, debugFlag))

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='qei-ltx1', help='env')
  parser.add_option('-r', '--redeploy', action='store_true', help='only do deploy')
  parser.add_option('--skipClean', action='store_true', help='skip clean')
  parser.add_option('--skipCfg', action='store_true', help='skip cfg')
  parser.add_option('--skipDebug', action='store_true', help='skip debug')
  parser.add_option('--skipAssert', action='store_true', help='skip assert')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if (len(args) < 1):
    parser.print_help()
    exit()

  main(args)
