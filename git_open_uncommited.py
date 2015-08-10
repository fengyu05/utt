#!/usr/bin/python

"""
Grasp all files in a changelist and open it in vim
"""
import sys
import os
import subprocess

def main(argv):

  uncommitStartLine = "Changes to be committed:"
  otherStartedLine = "Changes not staged for commit:"

  ps = subprocess.Popen('git status',
      shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  output = ps.communicate()[0]
  lines = output.split('\n')

  modifyFiles = []

  started = False
  for line in lines:
    if started:
      if line.find(otherStartedLine) != -1:
        started = False
        continue
    else:
      if line.find(uncommitStartLine) != -1:
        started = True
      continue

    if line.find('new file:') != -1:
      modifyFiles.append(line.split(':')[1].strip())
    if line.find('modified:') != -1:
      modifyFiles.append(line.split(':')[1].strip())

  print 'Found modified files:---------------'
  for line in modifyFiles:
    print line
  print 'List files end --------------------'

  allFiles = ' '.join(modifyFiles)

  print allFiles

  cmd = 'vim %s' % (allFiles)
  os.system(cmd)

if __name__ == '__main__':
  main(sys.argv)


