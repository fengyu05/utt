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
  print 'list jar file:%s' % sys.argv[1]
  show_jar_classes(sys.argv[1])


if __name__ == '__main__':
  main()
