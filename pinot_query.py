#!/usr/bin/python

import sys
import urllib


if len(sys.argv) < 3:
  print '%s url query' % sys.argv[0]
  sys.exit(1)

pinotPath = sys.argv[1]
pinotQuery = sys.argv[2]

params = urllib.urlencode({'q': 'statistics', 'bqlRequest': pinotQuery})

print '%s?%s' % (pinotPath, params)
result = urllib.urlopen("%s?%s" % (pinotPath, params))

print result.read()



