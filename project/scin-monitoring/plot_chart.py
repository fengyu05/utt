#!/usr/bin/python
"""
Plot multi trend in one graph.
Input: name,date,value
"""
__author__ = 'zhdeng'
__version__ = '1'

import sys, os, time, datetime, glob, uuid
import numpy as np 

from matplotlib import pyplot
import pylab
from pylab import xticks

SCATTER = 'scatter' #name, valueX, valueY
TREND = 'trend' #name, second/millissceond, value

RESULT_DIR = 'results'

options = dict()


def loadInput():
  inputDir = options.inputDir
  if options.inputFolder:
    assert os.path.exists(options.inputFolder)
    filenames = glob.glob('%s/*' % options.inputFolder)
    uid = str(uuid.uuid4())
    inputDir = '/tmp/%s' % uid
    print 'Merge %s to %s' % (filenames, inputDir)
    with open(inputDir, 'wb') as outfile:
      for fname in filenames:
        with open(fname, 'r') as readfile:
          for line in readfile.read():
            outfile.write(line)

  assert os.path.exists(inputDir), 'input(%s) not exist' % inputDir
  dataByName = dict()
  if options.singleSource:
    print 'Signle Trend input'
    data = np.loadtxt(inputDir, delimiter = options.delimiter,
      dtype = {'names' : ('valueX', 'valueY'),
               'formats' : ('f8', 'f8')}) 
    name = 'default' 
    if options.title:
      name = options.title
    if options.outputFile == 'multi_trend':
      options.outputFile = 'single_trend'
    dataByName[name] = []
    for record in data:
      dataByName[name] += [(record[0], record[1])]
  else:
    data = np.loadtxt(inputDir, delimiter = options.delimiter,
      dtype = {'names' : ('name', 'valueX', 'valueY'),
               'formats' : ('S128', 'f8', 'f8')}) 
    for record in data:
      name = record[0]
      if name not in dataByName:
        dataByName[name] = []
      dataByName[name] += [(record[1], record[2])]

  toRemoveList = []
  if options.useMask:
    masks = options.useMask.split(',')
    for mask in masks:
      for name in dataByName.iterkeys():
        if mask.endswith('*'):
          if name.startswith(mask[:-1]):
            print 'remove %s because of filter:%s' % (name, mask)
            toRemoveList.append(name)
        else:
          if name == mask:
            print 'remove %s because of filter:%s' % (name, mask)
            toRemoveList.append(name)

  for removeName in toRemoveList:
    del dataByName[removeName]

  return dataByName


def configChart(figure):
  cf = pylab.gcf()
  defaultSize = cf.get_size_inches()
  plotSizeXRate = options.plotSizeXRate and options.plotSizeXRate or options.plotSizeRate 
  plotSizeYRate = options.plotSizeYRate and options.plotSizeYRate or options.plotSizeRate 
  cf.set_size_inches( (defaultSize[0]*plotSizeXRate, defaultSize[1]*plotSizeYRate) )

  ax = figure.add_subplot(111)
  ax.set_xlabel(options.xlabel)
  ax.set_ylabel(options.ylabel)
  ax.set_title('%s' %
    (options.title and options.title or options.outputFile))

  return ax 

def ensureDir(dirName):
  """
  Create directory if necessary.
  """
  if not os.path.exists(dirName):
    os.makedirs(dirName)

def outputGraph(figure):
  ensureDir(RESULT_DIR)
  figure.savefig('%s/%s.png' % (RESULT_DIR, options.outputFile))
  pyplot.close()

def plotData(dataByName):
  figure = pyplot.figure()
  ax = configChart(figure)

  if options.chart == SCATTER:
    plotScatter(dataByName, ax)
  elif options.chart == TREND:
    plotTrend(dataByName, ax)

  if not options.legendOff:
    ax.legend(loc='upper right', shadow=True)
  outputGraph(figure)

def plotScatter(dataByName, ax):
  for (name, data) in dataByName.iteritems():
    colors = np.random.rand(128)
    (valueX, valueY) = zip(*data)
    ax.scatter(valueX, valueY, c=colors, label=name)

  if options.useDateOnX:
    useDateOnX()

def plotTrend(dataByName, ax):
  for (name, data) in dataByName.iteritems():
    (date, value) = zip(*data)
    ax.plot(date, value, label=name)
  useDateOnX()

def useDateOnX():
  locs,labels = xticks()
  timeUnix = 1.0
  if options.useMillis:
    timeUnix = 1000.0
  xticks(locs, map(lambda x:
      datetime.datetime.fromtimestamp(x/timeUnix).strftime('%m/%d'), locs))
  

def main():
  dataByName = loadInput()
  plotData(dataByName)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()

  parser.add_option('--chart', dest='chart', default=SCATTER, help='chart type')

  parser.add_option('-f', '--file', dest='inputDir', default='',
    help='Path to input file or directory. Input format: CSV by --delimiter: len(rocord)==3. Ex: name, value, value')

  parser.add_option('--folder', dest='inputFolder', default='',
    help='Path to input folder or directory. Input format: CSV by --delimiter: len(rocord)==3. Ex: name, value, value')

  parser.add_option('-d', '--delimiter', dest='delimiter', default='\t',
    help='CSV field delimiter.')

  parser.add_option('-o', '--out', dest='outputFile', default='output', help='output file')

  parser.add_option('-t', '--title', dest='title', default='', help='')

  parser.add_option('-y', '--ylabel', dest='ylabel', default='',
    help='')
  parser.add_option('-x', '--xlabel', dest='xlabel', default='',
    help='')
  parser.add_option('-s', '--single', dest='singleSource',
    action='store_true', help='data only has single source.(Two column)')

  parser.add_option('-r', '--rate', type='float', dest='plotSizeRate', default=2.0, help='')
  parser.add_option('--rateX', type='float', dest='plotSizeXRate', default=0, help='')
  parser.add_option('--rateY', type='float', dest='plotSizeYRate', default=0, help='')

  parser.add_option('--dateX', dest='useDateOnX',
    action='store_true', help='use date on x axes')

  parser.add_option('--dateM', dest='useMillis',
    action='store_true', help='use millis')

  parser.add_option('-l', '--legendOff', dest='legendOff',
    action='store_true', help='dont plot legend')

  parser.add_option('--mask', dest='useMask', default='', help='mask certain data')

  (options,args) = parser.parse_args()
  if (not options.inputDir and not options.inputFolder):
    parser.print_help()
    exit()

  main()
