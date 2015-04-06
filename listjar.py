#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys
import zipfile
import glob

def show_jar_classes(jar_file):
  """prints out .class files from jar_file"""
  zf = zipfile.ZipFile(jar_file, 'r')
  try:
    lst = zf.infolist()
    for zi in lst:
      fn = zi.filename
      if fn.endswith('.class'):
        print(fn)
  finally:
    zf.close()


def main():
  from optparse import OptionParser
  parser = OptionParser()

  (options,args) = parser.parse_args()

  for arg in args:
    print 'list jar file:%s' % arg
    show_jar_classes(arg)


if __name__ == '__main__':
  main()
