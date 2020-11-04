#!/usr/bin/env python
""" Unique Words checker [Productivity Tool]
Scan the given file, list all the words appear only once.
It's very possible that these words are mis spell.
@Author: Zhifeng(fengyu05@gmail.com)
"""

usage = "usage: %prog [--min_length=5] filename"

import sys
import re
from optparse import OptionParser

parser = OptionParser(usage)
parser.add_option(
    "-l",
    "--min_length",
    dest="MIN_LENGTH",
    type="int",
    default=5,
    help="min length that concerns",
)


def checkWords(filename, options):
    content = open(filename, "r").readlines()
    wordDict = dict()
    for line in content:
        words = re.split("\W+", line)
        for word in words:
            if len(word) >= options.MIN_LENGTH:
                if word in wordDict:
                    wordDict[word] = wordDict[word] + 1
                else:
                    wordDict[word] = 1

    uniqWords = [word for word, frequent in wordDict.iteritems() if frequent == 1]
    print uniqWords


def main():
    (options, argv) = parser.parse_args()
    if len(argv) < 1:
        parser.error("incorrect number of arguments")
        sys.exit(1)
    filename = argv[0]
    checkWords(filename, options)


if __name__ == "__main__":
    main()
