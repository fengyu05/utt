#!/usr/bin/env python
""" Frequent Words extractor [Productivity Tool]
Scan the given directory, list all the words appear in certain type of files
Generator a list of that words
Mainly for vim completion
@Author: Zhifeng(fengyu05@gmail.com)
"""

usage = "usage: %prog [--min_length=5] [--min_fre=5] filetype directory"

import sys
import re
from optparse import OptionParser
from os import listdir
from os.path import isdir,islink,join

parser = OptionParser(usage)
parser.add_option("-l", "--min_length", dest="MIN_LENGTH",
                  type="int",
                  default = 7,
                  help="min length that concerns")

parser.add_option("-f", "--min_freq", dest="MIN_FREQUENT",
                  type="int",
                  default = 7,
                  help="min frequent that concerns")

parser.add_option("-d", "--max_deep", dest="MAX_DEEP",
                  type="int",
                  default = 20,
                  help="max deep of directory")

wordDict = dict()

def checkWords(filetype, directory, options, deep):
  if deep > options.MAX_DEEP:
    return
  for file in listdir(directory):
    fileFullPath = join(directory, file)
    if isdir(fileFullPath) and not islink(fileFullPath):
      checkWords(filetype, fileFullPath, options, deep + 1)
    else:
      if fileFullPath.endswith("." + filetype):
        content = open(fileFullPath, "r").readlines()
        for line in content:
          words = re.split('\W+', line)
          for word in words:
            if len(word) >= options.MIN_LENGTH:
              if word in wordDict:
                wordDict[word] = wordDict[word] + 1
              else:
                wordDict[word] = 1

def genWords(options):
  freqWords = [word for word, frequent in wordDict.iteritems() 
               if frequent >= options.MIN_FREQUENT]
  for word in freqWords:
    print (word)

def main():
  (options, argv) = parser.parse_args()
  if len(argv) < 2:
    parser.error("incorrect number of arguments")
    sys.exit(1)
  filetype = argv[0]
  directory = argv[1]
  checkWords(filetype, directory, options, 0)
  genWords(options)


if __name__ == '__main__':
  main()
