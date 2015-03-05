#!/usr/bin/python

"""
Grasp all git unstaged files and do git add
"""
import sys
import os
import subprocess

def main(argv):

  ps = subprocess.Popen('git status',
      shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  output = ps.communicate()[0]
  lines = output.split('\n')

  modifyFiles = []

  started = False
  for line in lines:
    if len(line) <= 1:
      continue
    line = line[1:].strip() # remove '#' and space

    if line.startswith('Changes not staged for commit:'):
      started = True
      continue
    elif line.startswith('Untracked files:'):
      break
    elif started and line.startswith('modified:'):
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

  cmd = 'git add %s' % (allFiles)
  print cmd
  assert os.system(cmd) == 0

if __name__ == '__main__':
  main(sys.argv)
