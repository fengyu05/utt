#!/usr/bin/env python
""" Random generate char replace content in html file
A detailed description of junkcodehtml.
"""

import sys
import random
from HTMLParser import HTMLParser

MEANLINGFUL_STRING_LEN = 3

def randLowerCase():
    return chr(random.randint(ord('a'), ord('z')))

def randUperCase():
    return chr(random.randint(ord('A'), ord('Z')))

def genChar(char):
  if char.isspace():
    return char
  if ord(char) > 128:
    return randLowerCase() + "."
  if random.random() > 0.5:
    return randUperCase()
  else:
    return randLowerCase()

def hasLongChar(s):
  for char in s:
    if ord(char) > 128:
      return True
  return False

class MyHtmlParser(HTMLParser):
  newContent = u""

  def junkCode(self, data):
    newData = ""
    for char in data:
      newData += genChar(char)
    return newData



  def handle_data(self, data):
    if (len(data) > MEANLINGFUL_STRING_LEN or hasLongChar(data)):
      newData = self.junkCode(data)
      self.newContent = self.newContent.replace(data, newData, 1)

  def replaceWithJunkCode(self, content):
    self.newContent = content
    self.feed(content)
    return self.newContent





def main(argv):
  pass


def main(argv):
  if len(argv) < 2:
    print 'junkcodehtml.py filename'
    return
  fileName = argv[1]
  content = ""
  with open(fileName, 'r') as f:
    content = f.read()

  content = content.decode("utf-8")
  parser = MyHtmlParser()
  content = parser.replaceWithJunkCode(content)

  content = content.encode('utf-8')
  outputFileName = fileName.rstrip(".html") + ".junk.html"
  with open(outputFileName, 'w') as f:
    f.write(content)
    f.close()


if __name__ == '__main__':
  main(sys.argv)
