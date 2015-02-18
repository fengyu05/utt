#!/usr/bin/python

"""
Read files from stdin pile, display a quick reference link, and set envvar.
"""
import sys, os
import time

RESET_CODE = '\033[0m'
GREEN_CODE = '\033[1;32m'

def main(argv):
  try:
    index = 1
    for line in sys.stdin:
      if index % 2 == 0:
        sys.stdout.write(GREEN_CODE)

      line = line.strip()
      print '[F%d]' % index, line
      os.system('export F%d=%s' % (index, line))

      sys.stdout.write(RESET_CODE)

      index = index + 1
  except KeyboardInterrupt:
    sys.stdout.flush()

if __name__ == '__main__':
  main(sys.argv)


