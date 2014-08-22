#!/usr/bin/python
""" Java import fixer [Productivity Tool]
Dedup and sort java import.
"""
import sys
import os
import uuid


def main(argv):
  if len(argv) < 2:
    print '%s filename' % argv[0]
    return
  fileName = argv[1]
  preLines = []
  lines = []
  postLines = []
  found = False

  with open(fileName, 'r') as f:
    for line in f:
      if line.startswith('import ') or line.startwith('package '):
        lines.append(line)
        found = True
      else:
        if found:
          postLines.append(line)
        else:
          preLines.append(line)

  lines = list(set(lines)) #unique lines

  print "After sort -------------------------------------------------"
  for line in lines:
    print line
  print "Result end -------------------------------------------------"

  lines = preLines + lines + postLines

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


