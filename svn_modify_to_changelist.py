#!/usr/bin/python

""" 
Grasp all svn update without changelist to change list
"""
import sys
import os
import subprocess

def main(argv):
  if len(argv) < 2:
    print '%s changelist' % argv[0]
    return

  ps = subprocess.Popen('svn st',
      shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  output = ps.communicate()[0]
  lines = output.split('\n')

  modifyFiles = []

  for line in lines:
    if line.startswith('--- Changelist'):
      break
    if line.startswith('M'):
      modifyFiles.append(line.split('M')[-1].strip())
    if line.startswith('A'):
      modifyFiles.append(line.split('A')[-1].strip())

  print 'Found modified files:---------------'
  for line in modifyFiles:
    print line
  print 'List files end --------------------'

  allFiles = ' '.join(modifyFiles) 

  cmd = 'svn changelist %s %s' % (argv[1], allFiles)
  print cmd
  assert os.system(cmd) == 0

if __name__ == '__main__':
  main(sys.argv)
