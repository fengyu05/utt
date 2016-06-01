#!/usr/bin/python
""" Avro [Productivity Tool]
Write an avro file
"""
import os, io, sys
import avro, json
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


ACTION_WRITE = 'write'
ACTION_PRINT = 'print'

def printHelp():
  print 'avro_utt action args'

def printAvro(inputPath):
  reader = DataFileReader(open(inputPath, "r"), DatumReader())
  for data in reader:
    print data
  reader.close()

def flattenUnionValue(unionValue):
  if type(unionValue) == dict:
    for k, v in unionValue.iteritems():
      if k == 'string' or k == 'double' or k == 'long' or k == 'int' or k == 'boolean':
        return v
  else:
    return unionValue

def flattenUnion(record):
  for k, v in record.iteritems():
    record[k] = flattenUnionValue(v)

  return record


def writeAvro(schemaPath, dataPath):
  schema = avro.schema.parse(open(schemaPath).read())
  schemaBaseName = os.path.basename(schemaPath).split('.')[0]

  writer = DataFileWriter(open(schemaBaseName + ".avro", "w"), DatumWriter(), schema)

  data = json.loads(io.open(dataPath).read())
  for record in data:
    record = flattenUnion(record)
    print record
    writer.append(record)
  writer.close()

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--env', default='dev', help='env')

  (options,args) = parser.parse_args()

  print 'options:', options
  print 'args:', args
  print '\n\n'

  if (len(args) < 1):
    parser.print_help()
    printHelp()
    exit()

  ALL_ACTION = {
             ACTION_WRITE: writeAvro,
             ACTION_PRINT: printAvro,
             }

  action = args[0]
  if action in ALL_ACTION:
    ALL_ACTION[action](*args[1:])

    print ('\n\n')
  else:
    printHelp()
