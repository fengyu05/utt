#!/usr/bin/python
"""
Plot chart with CSV
Help: -h
"""
__author__ = 'zhdeng'
__version__ = '1.2'

import sys, os, time, datetime, glob, uuid, io, random, getpass, fnmatch
os.environ["DISPLAY"] = ":0.0"

from matplotlib import pyplot
import pylab
import numpy as np
from pylab import xticks

SCATTER = 'scatter' #name, valueX, valueY
TREND = 'trend' #name, second/millissceond, value
QUANTILE = 'quantile' #name,low,mid,high

RESULT_DIR = 'results'

LABEL_COLUMN = 'label'
TIME_COLUMN = 'time'
QUANTILE_COLUMN = 'quantile' #Format: low:mid:hight e.g  25:50:100

REMOTE_FILE_CACHE_PATH = '~/.plot_chart_file_cache'

MS_GUARD = 10000000000

options = dict()

ENV_HOLDEM = 'holdem'
ENV_WAR = 'war'

HOST = {
  ENV_HOLDEM: 'ltx1-holdemgw01.grid.linkedin.com',
  ENV_WAR: 'lva1-wargw01.grid.linkedin.com',
}


class Data:
  def __init__(self, name):
    self.name = name
    self.series = []

  def addSeriesPoint(self, key, value):
    self.series.append((key, value))

  def getSeries(self):
    return self.series

def printRun(cmd):
  print cmd
  assert os.system(cmd) == 0

def mergeInputFiles(inputFolder):
  assert os.path.exists(options.inputFolder), 'Folder not exist'
  filenames = glob.glob('%s/*' % options.inputFolder)
  uid = str(uuid.uuid4())
  inputDir = '/tmp/%s' % uid
  print 'Merge %s to %s' % (filenames, inputDir)
  with open(inputDir, 'wb') as outfile:
    for fname in filenames:
      with open(fname, 'r') as readfile:
        for line in readfile.read():
          outfile.write(line)
  assert os.path.exists(inputDir)
  return inputDir

def copyFromGateway(inputFolder, hidden, env=ENV_HOLDEM):
  if env not in HOST:
    print 'Noknown host env  %s' % env
    exit(1)
  host = HOST[env]
  username = getpass.getuser()
  if hidden:
    target = '/tmp/data/'
  else:
    target = './data/'

  basename = os.path.basename(inputFolder)
  #assert basename, 'terget basename is empty'
  rmCmd = 'rm -rf %s' % (target + basename)
  printRun(rmCmd)
  cmd1 = 'ssh -q -K -tt %s "rm -rf %s;mkdir %s;hadoop fs -copyToLocal %s %s/"' % (host, REMOTE_FILE_CACHE_PATH, REMOTE_FILE_CACHE_PATH, inputFolder, REMOTE_FILE_CACHE_PATH)
  printRun(cmd1)
  renameTarget = target + basename + '/' + str(uuid.uuid4())
  printRun('mkdir -p %s' % renameTarget)
  cmd2 = 'scp -r %s@%s:%s/%s/* %s' % (username, host, REMOTE_FILE_CACHE_PATH, basename, renameTarget)
  printRun(cmd2)
  return renameTarget


def find_files(directory, pattern):
  for root, dirs, files in os.walk(directory):
    for basename in files:
      if fnmatch.fnmatch(basename, pattern):
        filename = os.path.join(root, basename)
        yield filename


def mergeInputFilesFromHdfs(inputPathList, hiddenTmp):
  uid = str(uuid.uuid4())
  mergedFile = '/tmp/%s' % uid
  for inputPath in inputPathList:
    inputPathFields = inputPath.split(':')
    if len(inputPathFields) == 2:
      absPath = copyFromGateway(inputPathFields[1], hiddenTmp, inputPathFields[0])
    elif len(inputPathFields) == 1:
      absPath = copyFromGateway(inputPathFields[0], hiddenTmp)
    else:
      print 'Unexpected input path for hdfs %s' % inputPath
      exit(1)
    assert os.path.exists(absPath), 'Couldn\'d locate hdfs file local folder: %s' % absPath

    #filenames = glob.glob('%s/*' % absPath)
    filenames = find_files('%s' % absPath, '*')

    for filename in filenames:
      os.system('cat %s >> %s' % (filename, mergedFile))

  assert os.path.exists(mergedFile)
  return mergedFile

def splitInputList(input):
  return input.split(',')

def selectNotEmpty(array):
  for value in array:
    if value:
      return value
  return None

def loadInput():
  # merage input files
  inputDir = options.inputDir
  if options.inputFolder:
    inputDir = mergeInputFiles(options.inputFolder)
  elif options.hdfsFolder:
    inputDir = mergeInputFilesFromHdfs(splitInputList(options.hdfsFolder), True)
  elif options.hdfsFolder2:
    inputDir = mergeInputFilesFromHdfs(splitInputList(options.hdfsFolder2), False)

  if not options.outputFile:
    options.outputFile = os.path.basename(selectNotEmpty([options.inputDir, options.inputFolder, options.hdfsFolder, options.hdfsFolder2]))

  print('open file %s' % inputDir)
  # read file to columns
  columns = []
  columnsInit = False
  for line in io.open(inputDir).readlines():
    fields = line.split(options.delimiter)
    if not columnsInit:
      columnsInit = True
      for i in xrange(len(fields)):
        columns.append(list())
    for i in xrange(len(columns)):
      columns[i].append(fields[i])

  print("Column size:" + str(len(columns)))

  # read columns name
  columnNames = []
  if options.columnName:
    names = options.columnName.split(',')
    for name in names:
      columnNames.append(name)
    for i in xrange(len(names), len(columns)):
      columnNames.append('c%d' % i)
  else:
    print("Auto apply column names")
    columnNames.append(LABEL_COLUMN)
    for i in xrange(1, len(columns)):
      columnNames.append('c%d' % i)

  print("columnNames:" + str(columnNames))

  if len(columnNames) == 2:
    for x in columnNames: # 2 column table shouldn't have label
      assert x != LABEL_COLUMN, '2 column table shouldn\'t have label'

    columnNames.append(LABEL_COLUMN)
    labelColumn = ['_'] * len(columns[0])
    columns.append(labelColumn)

    print("After append label: columnNames:" + str(columnNames))

  if not options.kColumn:
    for x in columnNames:
      if x != LABEL_COLUMN: # select first not label column
        options.kColumn = x
        break

  if not options.xLabel:
    print ('select x label %s' % options.kColumn)
    options.xLabel = options.kColumn

  # convert columns data
  labelColumn = None
  kColumn = None
  dataColumns = {}
  for i in xrange(len(columns)):
    columnName = columnNames[i]
    if columnName == LABEL_COLUMN:
      labelColumn = columns[i]
      continue
    elif columnName == TIME_COLUMN:
      options.kColumn = TIME_COLUMN
      options.hasTrend = True
      timeUnit = 1.0
      if options.useMillis or float(columns[i][0]) > MS_GUARD:
        timeUnit = 1000.0
      columns[i] = [ float(x)/timeUnit for x in columns[i]]
    elif columnName == QUANTILE_COLUMN:
      columns[i] = [ [ float(x) for x in x.split(':')] for x in columns[i]]
    else:
      columns[i] = [ float(x) for x in columns[i]]

    if columnName == options.kColumn:
      kColumn = columns[i]

    if columnName != options.kColumn:
      if not options.yLabel:
        print ('select y label %s' % columnName)
        options.yLabel = columnName #use first data column as yLabel

      dataColumns[columnNames[i]] = columns[i]

  assert(labelColumn != None)
  assert(kColumn != None)
  assert len(labelColumn) == len(kColumn), 'Size: %d != %d' %(len(labelColumn), len(kColumn))

  # convert to Data record
  dataByName = dict()
  for columnName, column in dataColumns.iteritems():
    assert(len(labelColumn) == len(column))
    for i in xrange(len(column)):
      if len(dataColumns) == 1:
        name = labelColumn[i]
      else:
        name = labelColumn[i] + ':' + columnName
      assert name, "data name is empty"
      if not name in dataByName:
        dataByName[name] = Data(name)

      key = kColumn[i]
      value = column[i]
      dataByName[name].addSeriesPoint(key, value)

  # Use data mask or whitelist 
  if options.useMask or options.whitelist:
    dataByName = removeMaskData(dataByName)

  #print ("DataByName:" + str(dataByName.keys()))
  return dataByName

def removeMaskData(dataByName):
  # Whitelist serves first
  if not options.whitelist:
    toRemoveList = []
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

  if options.whitelist:
    print 'Use whitelist'
    whitelists = set()
    for whitelist in options.whitelist.split(','):
      for name in dataByName.iterkeys():
        if whitelist.endswith('*'):
          if name.startswith(whitelist[:-1]):
            print 'whitelist %s because of filter:%s' % (name, whitelist)
            whitelists.add(name)
        else:
          if name == whitelist:
            print 'whitelist %s because of filter:%s' % (name, whitelist)
            whitelists.add(name)

    if whitelists:
      dataByName = dict([(k, v) for k, v in dataByName.iteritems() if k in whitelists])

  return dataByName

def configChart(figure):
  cf = pylab.gcf()
  defaultSize = cf.get_size_inches()
  plotSizeXRate = options.plotSizeXRate and options.plotSizeXRate or options.plotSizeRate 
  plotSizeYRate = options.plotSizeYRate and options.plotSizeYRate or options.plotSizeRate 
  cf.set_size_inches( (defaultSize[0]*plotSizeXRate, defaultSize[1]*plotSizeYRate) )

  ax = figure.add_subplot(111)
  ax.set_xlabel(options.xLabel)
  assert(options.yLabel)
  ax.set_ylabel(options.yLabel)
  ax.set_title('%s' %
    (options.title and options.title or options.outputFile))


  ax.grid(True)

  return ax

def ensureDir(dirName):
  """
  Create directory if necessary.
  """
  if not os.path.exists(dirName):
    os.makedirs(dirName)

def outputGraph(figure):
  ensureDir(RESULT_DIR)
  outputName = '%s/%s.png' % (RESULT_DIR, options.outputFile)
  print('outputFile:' + outputName)
  figure.savefig('%s/%s.png' % (RESULT_DIR, options.outputFile))
  cmd = 'gthumb %s/%s.png &' % (RESULT_DIR, options.outputFile)
  if not options.gthumbOff:
    print(cmd)
    os.system(cmd)
  pyplot.close()

def applyLim(ax):
  if options.xlim:
    xlim = options.xlim.split(',')
    xlim = [ int(x) for x in xlim ]
    if len(xlim) == 1:
      print 'applying xlim %s' % xlim
      pyplot.xlim((0, xlim[0]))
    elif len(xlim) >= 2:
      print 'applying xlim %s' % xlim
      ax.set_xlim((xlim[0], xlim[1]))

  if options.ylim:
    print 'applying ylim %s' % options.ylim
    ylim = options.ylim.split(',')
    ylim = [ int(x) for x in ylim ]
    if len(ylim) == 1:
      ax.set_ylim((0, ylim[0]))
    elif len(ylim) >= 2:
      ax.set_ylim((ylim[0], ylim[1]))

def plotData(dataByName):
  figure = pyplot.figure()
  ax = configChart(figure)

  if options.chart == SCATTER:
    plotScatter(dataByName, ax)
  elif options.chart == TREND:
    plotTrend(dataByName, ax)
  elif options.chart == QUANTILE:
    plotQuantile(dataByName, ax)
  else:
    print 'Unknown chart type'
    exit(1)

  if not options.legendOff:
    ax.legend(loc='upper right', shadow=True)

  if options.kColumn == TIME_COLUMN:
    useTimeOnX()

  applyLim(ax)
  outputGraph(figure)

def plotScatter(dataByName, ax):
  for (name, data) in dataByName.iteritems():
    colors = np.random.rand(128)
    (valueX, valueY) = zip(*data.getSeries())
    ax.scatter(valueX, valueY, c=colors, label=name)

def plotTrend(dataByName, ax):
  for (name, data) in dataByName.iteritems():
    (date, value) = zip(*sorted(data.getSeries()))
    ax.plot(date, value, label=name)

def plotQuantile(dataByName, ax):
  quantiles = []
  values = []
  for (name, data) in dataByName.iteritems():
    colors = np.random.rand(128)
    values.append(data.getSeries()[0][0])
    quantiles.append(data.getSeries()[0][1])

  ax.boxplot(quantiles)

def useTimeOnX():
  print ('use time on X axes')
  locs,labels = xticks()
  xticks(locs, map(lambda x:
      datetime.datetime.fromtimestamp(x).strftime('%m/%d/%Y'), locs))

def printExample():
  print '''
  1. Plot a trend line on local:
    plot_chart.py -c 'label,date,value' -f input.csv
  2. Plot a trend line on hdfs:
    plot_chart.py -c 'label,date,value' --hdfs'/job/fcst/...

  3. Plot a scatter on local:
    plot_chart.py --chart scatter -f input.csv -c 'label,value'
  '''

def main():
  dataByName = loadInput()
  plotData(dataByName)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()

  parser.add_option('-f', '--file', dest='inputDir', default='',
    help='Path to input file. Input format file:CSV by --delimiter')

  parser.add_option('--folder', dest='inputFolder', default='',
    help='Path to input directory. Input format file: CSV by --delimiter')

  parser.add_option('--hdfs', dest='hdfsFolder', default='',
    help='Path to input hdfs directory. Input file format: CSV by --delimiter')

  parser.add_option('--hdfs2', dest='hdfsFolder2', default='',
    help='Path to input hdfs directory. Input file format: CSV by --delimiter')

  parser.add_option('-d', '--delimiter', dest='delimiter', default='\t', help='CSV field delimiter. Default to Tab(\\t)')

  parser.add_option('--chart', dest='chart', default=TREND, help='Chart type: \'trend\' or \'scatter\'. Default to trend')

  parser.add_option('-o', '--out', dest='outputFile', default='', help='Output file name. Will auto append .png extention')

  parser.add_option('-t', '--title', dest='title', default='', help='Chart title. Default to use output file name')

  parser.add_option('-c', '--column', dest='columnName', default='', help='Name of each column, separated by comma. Ex: \'label,time,count\'.\n \'label\' is a reserved keyword to specify data collection label. \'time\' is a reserved keyword to specify timestamp column')

  parser.add_option('-k', '--kColumn', dest='kColumn', default='', help='Key column. By default use time column as key(x) column.')

  parser.add_option('-x', dest='xLabel', default='', help='X column label')
  parser.add_option('-y', dest='yLabel', default='', help='Y column label')

  parser.add_option('--xlim', dest='xlim', default='', help='X limit')
  parser.add_option('--ylim', dest='ylim', default='', help='Y limit')

  parser.add_option('-r', '--rate', type='float', dest='plotSizeRate', default=1.5, help='Chart size rate.')
  parser.add_option('--rateX', type='float', dest='plotSizeXRate', default=0, help='Chart length rate')
  parser.add_option('--rateY', type='float', dest='plotSizeYRate', default=0, help='Chart height rate')

  parser.add_option('--millis', dest='useMillis', action='store_true', help='use milli second in timestamp. Timestampe bigger than 10^10 will automatically apply this option')

  parser.add_option('-l', '--legendOff', dest='legendOff', action='store_true', help='Don\'t plot legend.')

  parser.add_option('--gthumbOff', dest='gthumbOff', action='store_true', help='Don\'t open result png file.')

  parser.add_option('--mask', dest='useMask', default='', help='mask certain data. Ex \'metric_nus*,metric_supply*\'. Will remove data collection label start with \'metric_nus and metric_supply\'')

  parser.add_option('--whitelist', dest='whitelist', default='', help='whitelist certain data. Ex \'metric_nus*,metric_supply*\'. Will filter other data collection besides the one start with \'metric_nus and metric_supply\'')

  (options,args) = parser.parse_args()
  if (not (options.inputDir or options.inputFolder or options.hdfsFolder or options.hdfsFolder2)):
    parser.print_help()
    printExample()
    exit()

  main()
