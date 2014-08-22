#!/usr/bin/env python
""" Niter [Productivity Tool]
remove duplicate empty line, line ending spaces
"""
import sys
import os
import uuid

def isEmptyLine(line):
  return len(line.strip()) == 0

def stripEnd(line):
  return line.rstrip()

def main(argv):
  if len(argv) < 2:
    print 'nit.py filename'
    return
  fileName = argv[1]
  lines = []
  prevIsEmpty = False
  with open(fileName, 'r') as f:
    for line in f:
      if isEmptyLine(line):
        if prevIsEmpty:
          continue
        prevIsEmpty = True
      else:
        prevIsEmpty = False

      lines.append(stripEnd(line) + '\n')
  homeDir = os.environ['HOME']
  backupFileName = str(uuid.uuid4())
  backupPath = homeDir + "/.backup/" + backupFileName
  print "Backup Path:", backupPath
  os.system("mkdir -p " + homeDir + "/.backup")
  os.system("cp " + fileName + " " + backupPath)

  with open(fileName, 'w') as f:
    f.writelines(lines)
    f.close()

if __name__ == '__main__':
  main(sys.argv)
