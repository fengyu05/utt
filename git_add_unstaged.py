#!/usr/bin/python

"""
Grasp all git unstaged files and do git add
"""
import sys
import os
import subprocess

options = dict()
args = list()

def main(args):

  ps = subprocess.Popen('git status',
      shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  output = ps.communicate()[0]
  lines = output.split('\n')

  modifyFiles = []

  started = False
  for line in lines:
    if len(line) <= 1:
      continue
    # remove '#' and space
    line = line.strip()
    if line[0] == '#':
        line = line[1:]
    line = line.strip()

    if line.startswith('Changes not staged for commit:'):
      started = True
      continue
    elif line.startswith('Untracked files:'):
      break
    elif started and (line.startswith('modified:') or line.startswith('deleted:')):
      fileds = line.split(':')
      assert len(fileds) == 2, 'modified format unknown'
      modifyFiles.append(fileds[1].strip())

  if len(modifyFiles) == 0:
    print 'Not unstaged file found'
    exit(1)
  print 'Found unstaged files:---------------'
  for line in modifyFiles:
    print line
  print 'List files end --------------------'

  allFiles = ' '.join(modifyFiles)

  if options.delete:
    print 'Include deleted'
    cmd = 'git add -u %s' % (allFiles) # include delete file
  else:
    cmd = 'git add %s' % (allFiles)
  print cmd
  assert os.system(cmd) == 0

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-d', '--delete', dest='delete', default=False, action='store_true', help='include delete')

  (options,args) = parser.parse_args()
  print options
  print args

  main(args)
