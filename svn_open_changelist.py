#!/usr/bin/python

"""
Grasp all files in a changelist and open it in vim
"""
import sys
import os
import subprocess

def main(argv):
  if len(argv) < 2:
    print '%s changelist' % argv[0]
    return
  target = argv[1]

  targetStartedLine = "--- Changelist '%s'" % target
  otherStartedLine = "--- Changelist"

  ps = subprocess.Popen('svn st',
      shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  output = ps.communicate()[0]
  lines = output.split('\n')

  modifyFiles = []

  started = False
  for line in lines:
    if started:
      if line.startswith(otherStartedLine):
        started = False
        continue
    else:
      if line.startswith(targetStartedLine):
        started = True
      continue

    if line.startswith('M'):
      modifyFiles.append(line[1:].strip())
    if line.startswith('A'):
      modifyFiles.append(line[1:].strip())
    if line.startswith('D'):
      modifyFiles.append(line[1:].strip())

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


