#!/usr/bin/python
""" Avro [Productivity Tool]
Print an avro file
"""
import sys
import avro
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


def main(argv):
  if len(argv) < 2:
    print '%s filename' % argv[0]
    return

  reader = DataFileReader(open(argv[1], "r"), DatumReader())
  for data in reader:
    print data
  reader.close()
  
if __name__ == '__main__':
  main(sys.argv)
