#!/usr/bin/python
"""
  [Produtivity tool]
  Return hadoop pig job remotely
"""
import os, getpass, io, shutil

__version__ = 0.2
__anthor__ = 'zhdeng'

env = dict()
options = dict()

ENV_MAGIC = 'magic'
ENV_NERTZ = 'nertz'
ENV_NERTZ2 = 'nertz2'
ENV_CANASTA = 'canasta'
ENV_WAR = 'war'

AZ_HOST = {
  ENV_MAGIC: 'eat1-magicgw01.grid.linkedin.com',
  ENV_CANASTA: 'eat1-canastagw01.grid.linkedin.com',
  ENV_NERTZ: 'eat1-nertzgw01.grid.linkedin.com',
  ENV_NERTZ2: 'eat1-nertzgw02.grid.linkedin.com',
  ENV_WAR: 'eat1-wargw01.grid.linkedin.com',
}


REMOTE_ROOT = '.pigHadoopEnv'
PIG = '/export/apps/pig/latest/bin/pig'
LOCAL_ROOT = '.pigHadoopEnv'
PIG_DEFAULT_PARAMS = [
'-Dmappred.child.env="JYTHONPATH=job.jar/Lib"',
'-Dpig.additional.jars=*.jar'
  ]

DEFAULT_PIG_PARAM = 'pigParam'


def getHost():
  return AZ_HOST[options.env]

def runCmd(cmd):
  print cmd
  assert os.system(cmd) == 0

def prepare():
  runCmd('mkdir -p %s' % (options.localDir))
  runCmd('ssh -q -K %s mkdir -p %s' % (getHost(), options.remoteDir))

def copyResouce(inputDir):
  resources = []
  if os.path.basename(inputDir).startswith('.'):
    print ('Ignore %s' % inputDir)
    return resources

  if os.path.isfile(inputDir):
    runCmd('cp -f %s %s' % (inputDir, options.projectDir))
    resources.append(inputDir)
  elif os.path.isdir(inputDir):
    for subpath in os.listdir(inputDir):
      resources += copyResouce(inputDir + '/' + subpath)
  else:
    assert False, '%s not exist' % inputDir

  return resources

def abspath(path):
  return os.path.abspath(os.path.expanduser(path.strip()))

def loadResource():
  resources = []
  print 'pwd', os.getcwd()
  assert os.path.exists(options.resource), 'resource file %s not exist' % options.resource
  options.project = os.path.basename(os.getcwd())
  options.projectDir = '%s/%s' % (options.localDir, options.project)
  runCmd('mkdir -p %s' % options.projectDir)
  for line in io.open(options.resource).readlines():
    newResouces = copyResouce(abspath(line))
    resources = resources + newResouces

  debugPrint(resources)

  if options.paramFile != DEFAULT_PIG_PARAM or os.path.exists(DEFAULT_PIG_PARAM): # DEFAULT_PIG_PARAM cant be abscent
    assert os.path.exists(options.paramFile), 'param file not exist'
    copyResouce(options.paramFile)
  return resources

def checkOverWrite(resources, target):
  resourcesMap = dict()
  for resource in resources:
    basename = os.path.basename(resource)
    if options.checkOverWrite and basename in resourcesMap:
      assert False, '%s duplicated %s:%s' % (basename, resourcesMap[basename], resource)
    resourcesMap[basename] = resource

  assert target in resourcesMap, 'Target: %s not in resources' % target


def rsync():
  resources = loadResource()
  runCmd('> %s/dump.jar' % options.projectDir)
  runCmd('rsync -av %s -e "ssh -q -K" %s:%s' %(options.projectDir, getHost(), options.remoteDir))
  return resources

def run(target):
  project = 'test'
  pigDefaultParams = ' '.join(PIG_DEFAULT_PARAMS)
  pigCmd = '%s %s -f %s ' %(options.pig, pigDefaultParams, target)

  if options.paramFile != DEFAULT_PIG_PARAM or os.path.exists(DEFAULT_PIG_PARAM):
    pigCmd += '-param_file %s ' % (options.paramFile)

  if options.dryrun:
    pigCmd += '--dryrun '


  remoteCmds = [
    'export PIG_UDFS=%s/%s' % (options.remoteDir, options.project),
    'cd %s/%s' %(options.remoteDir, options.project),
    pigCmd
    ]
  remoteCmd = ';'.join(remoteCmds)
  runCmd("ssh -q -K -tt %s '%s'" %(getHost(), remoteCmd))

def main(target):
  target = os.path.basename(target)
  print 'Target: %s' % target

  debugPrint('PWD:' + os.getcwd())
  prepare()
  resources = rsync()
  checkOverWrite(resources, target)

  run(target)

def extentOptions():
  options.remoteDir = '/export/home/%s/%s' % (options.user, options.remoteRoot)
  options.localDir = '%s/%s' % (os.getenv("HOME"), options.localRoot)

  debugPrint(options)

def debugPrint(msg):
  if options.debug == 'True':
    print (msg)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()

  parser.add_option('-f', '--file', dest='resource', default='resource.list', help='input resource list. One per line.')
  parser.add_option('-e', '--env', dest='env', default=ENV_NERTZ, help='Hadoop env')
  parser.add_option('-u', '--user', dest='user', default=getpass.getuser(), help='user name')
  parser.add_option('-d', '--debug', dest='debug', default='False', help='debug mode')
  parser.add_option('-p', '--param', dest='paramFile', default=DEFAULT_PIG_PARAM, help='pig param file')
  parser.add_option('--remote', dest='remoteRoot', default=REMOTE_ROOT, help='dir root to run the job')
  parser.add_option('--local', dest='localRoot', default=LOCAL_ROOT, help='local dir to cache resource')
  parser.add_option('--pig', dest='pig', default=PIG, help='pig cmd dir')
  parser.add_option('--checkOverWrite', dest='checkOverWrite', help='failed when duplciate input resouces exist', default=False)
  parser.add_option('--dryrun', dest='dryrun', help='', default=False, action='store_true')

  (options,args) = parser.parse_args()
  print 'options', options
  print 'args', args

  if (not len(args) > 0):
    parser.print_help()
    exit()

  extentOptions()

  main(args[0])
