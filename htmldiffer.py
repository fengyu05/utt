#!/usr/bin/env python
""" Html pretty Differ [Productivity Tool]
 differ two html file by dom tree
"""

import sys
import difflib



def main(argv):
  if len(argv) < 3:
    print 'htmldiffer.py file1 file2'
    return
  fileName1 = argv[1]
  fileName2 = argv[2]
  lines1 = open(fileName1, 'U').readlines();
  lines2 = open(fileName2, 'U').readlines();
  diff = difflib.HtmlDiff().make_file(lines1, lines2, fileName1, fileName2)

  sys.stdout.writelines(diff)


if __name__ == '__main__':
  main(sys.argv)
