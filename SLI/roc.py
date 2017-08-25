#!/usr/bin/python
"""
Generate ROC, PR and Correlation curves.
Format of input: Input format: CSV by --delimiter: len(rocord)==4. Ex: modelId, weight, score, label)
"""
__author__ = 'zhdeng'

import sys, os, time
os.environ["DISPLAY"] = ":0.0"
import bz2, gzip
import uuid
import heapq
import numpy as np

from collections import namedtuple
from multiprocessing import Process, Pool
from matplotlib import pyplot
import pylab


MERGE_DIR = 'merges'
SORT_DIR = 'sorts'
RESULT_DIR = 'results'

PHRASE_GROUP = 0
PHRASE_SORT = 1
PHRASE_PROCESS = 2
options = dict()

def openFile(file):
  """
  Handles opening different types of files (only normal files and bz2 supported)
  """
  file = file.lower()
  if file.endswith('.bz2'):
    return bz2.BZ2File(file)
  elif file.endswith('.gz'):
    return gzip.open(file)
  return open(file)

def ensureDir(dirName):
  """
  Create directory if necessary.
  """
  if not os.path.exists(dirName):
    os.makedirs(dirName)

def walktree(input):
  """
  Returns a list of file paths to traverse given input (a file or directory name)
  """
  if os.path.isfile(input):
    return [input]
  else:
    fileNames = []
    for root, dirs, files in os.walk(input):
      fileNames += [os.path.join(root, f) for f in files]
    return fileNames

def batchSort(input, output, key, bufferSize):
  """
  External sort on file using merge sort.
  See http://code.activestate.com/recipes/576755-sorting-big-files-the-python-26-way/
  """

  def merge(key=None, *iterables):
    if key is None:
      keyed_iterables = iterables
    else:
      Keyed = namedtuple("Keyed", ["key", "obj"])
      keyed_iterables = [(Keyed(key(obj), obj) for obj in iterable)
                for iterable in iterables]
    for element in heapq.merge(*keyed_iterables):
      yield element.obj

  from itertools import islice
  tempdir = '/tmp/' + str(uuid.uuid4())
  os.makedirs(tempdir)
  chunks = []
  try:
    with open(input,'rb',64*1024) as inputFile:
      inputIter = iter(inputFile)
      while True:
        current_chunk = list(islice(inputIter, bufferSize))
        if not current_chunk:
          break
        current_chunk.sort(key=key)
        output_chunk = open(os.path.join(tempdir,'%06i'%len(chunks)),'w+b',64*1024)
        chunks.append(output_chunk)
        output_chunk.writelines(current_chunk)
        output_chunk.flush()
        output_chunk.seek(0)
    with open(output,'wb',64*1024) as output_file:
      output_file.writelines(merge(key, *chunks))
  finally:
    for chunk in chunks:
      try:
        chunk.close()
        os.remove(chunk.name)
      except Exception:
        pass
  print "sorted file %s ready" % (output)

def calculateAUC(rocPoints):
  AUC = 0.0
  lastPoint = (0, 0)
  for point in rocPoints:
    AUC += (point[1] + lastPoint[1]) * (point[0] - lastPoint[0]) / 2
    lastPoint = point
  return AUC


def plotCurves(dataByModel):
  """
  Plot ROC, PR and Correlation Curves by model.
  """
  prFigure = pyplot.figure()
  configChart()
  prAx = prFigure.add_subplot(111)
  prAx.set_xlabel('Recall')
  prAx.set_ylabel('Precision')
  prAx.set_title('PR Curve')
  prAx.grid(True)

  rocFigure = pyplot.figure()
  configChart()
  rocAx = rocFigure.add_subplot(111)
  rocAx.set_xlabel('Fallout')
  rocAx.set_ylabel('Recall')
  rocAx.set_title('ROC Curve')
  rocAx.grid(True)

  corrFigure = pyplot.figure()
  configChart()
  corrAx = corrFigure.add_subplot(111)
  corrAx.set_xlabel('pCtr')
  corrAx.set_ylabel('eCtr')
  corrAx.set_title('Correlation Curve')
  corrAx.grid(True)

  cutoffXFigure = pyplot.figure()
  configChart()
  cutoffXAx = cutoffXFigure.add_subplot(111)
  cutoffXAx.set_xlabel('score')
  cutoffXAx.set_ylabel('rate')
  cutoffXAx.set_title('cutoff')
  cutoffXAx.grid(True)

  for (model, data) in dataByModel.items():
    (recalls, precisions) = zip(*(data['PR']))
    prAx.plot(recalls, precisions, marker='o', linestyle='--', label=model)

    (fallouts, recalls) = zip(*(data['ROC']))
    rocAx.plot(fallouts, recalls, marker='o', linestyle='--', label=model)

    (pCtrs, eCtrs) = zip(*(data['CORR']))
    corrAx.plot(pCtrs, eCtrs, label=model)

    (score, recall, fallout) = zip(*(data['cutoff']))
    cutoffXAx.plot(score, recall, label=model)
    cutoffXAx.plot(score, fallout, label=model)

  # saving figures
  ensureDir(RESULT_DIR)
  prAx.legend(loc='upper right', shadow=True)
  prFigure.savefig('%s/pr_curve.png' % RESULT_DIR)

  rocAx.legend(loc='upper right', shadow=True)
  rocFigure.savefig('%s/roc_curve.png' % RESULT_DIR)

  corrAx.legend(loc='upper center', shadow=True)
  corrFigure.savefig('%s/corr_curve.png' % RESULT_DIR)

  cutoffXAx.legend(loc='upper center', shadow=True)
  cutoffXFigure.savefig('%s/cutoff.png' % RESULT_DIR)

  pyplot.close()

  if not options.gthumbOff:
    cmd = 'gthumb %s/pr_curve.png %s/roc_curve.png %s/corr_curve.png %s/cutoff.png &' % (RESULT_DIR, RESULT_DIR, RESULT_DIR, RESULT_DIR)
    print(cmd)
    os.system(cmd)

def groupDataByModel(inputDir):
  """
  Group data to separated file by model.
  """
  t1 = time.time()
  print "merging files by model to %s" % MERGE_DIR
  ensureDir(MERGE_DIR)
  fileByModel = dict()
  for file in walktree(inputDir):
    for line in openFile(file):
      fields = line.split(options.delimiter)
      if options.ignoreInvalid:
        if len(fields) != 4 or fields[0] == '' or fields[1] == '' or fields[2] == '' or fields[3] == '':
          print 'Ingonre Invalid line', fields
          continue
      model = fields[0]
      if model not in fileByModel:
        fileByModel[model] = open('%s/%s.txt' % (MERGE_DIR, model), 'w')
      fileByModel[model].write(line)
  for file in fileByModel.values():
    file.close()
  t2 = time.time()
  print "merging files take %ss" % (t2 - t1)

  if options.useMask:
    fileByModel = removeMaskData(fileByModel)
  return fileByModel

def removeMaskData(dataByName):
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
  return dataByName

def loadFileNameByModel(inputDir):
  """
  Load the file names from a directory. Use to restart the process from a given phrase.
  """
  fileNames = walktree(inputDir)
  fileByModel = {}
  for file in fileNames:
    modelName = file.split('/')[-1]
    modelName = modelName.replace('.txt', '')
    fileByModel[modelName] = file
  return fileByModel

def sortDataFileByModel(fileByModel):
  """
  Use external sort to sort data file by score column.
  """
  t1 = time.time()
  print "sorting files...."
  ensureDir(SORT_DIR)
  processPool = []
  for model in fileByModel.keys():
    mergedFile = '%s/%s.txt' % (MERGE_DIR, model)
    sortedFile = '%s/%s.txt' % (SORT_DIR, model)
    if options.ignoreInvalid:
      key = eval('lambda l: -float(l.split("' + options.delimiter + '")[2] or 0.0)')
    else:
      key = eval('lambda l: -float(l.split("' + options.delimiter + '")[2])')
    process = Process(target = batchSort,
      args=(mergedFile, sortedFile, key, options.bufferSize))
    process.start()
    processPool.append(process)

  for process in processPool:
    process.join()
  t2 = time.time()
  print "sorting files take %ss" % (t2 - t1)

def processDataByModel(fileByModel):
  """
  Process data by model. Wait all the subprocess finish then plot curves together.
  """
  t1 = time.time()
  print "processing data...."
  pool = Pool(len(fileByModel))
  dataByModel = dict()
  resultList = []
  for model in fileByModel.keys():
    sortedFile = '%s/%s.txt' % (SORT_DIR, model)
    result = pool.apply_async(processData, args=(model, sortedFile))
    resultList.append(result)
  for result in resultList:
    try:
      (model, data) = result.get()
      dataByModel[model] = data
    except Exception, e:
      if not options.ignoreInvalid:
        raise e
  t2 = time.time()

  if options.aucSelect:
    selectLimit = options.selectLimit
    print 'Sort model by AUC and select top', selectLimit
    sortedModelTuple = sorted(dataByModel.items(), key=lambda item: item[1]['AUC'], reverse=True)
    dataByModel = dict(sortedModelTuple[:selectLimit])

  if options.verbose:
    print dataByModel
  plotCurves(dataByModel)
  print "processing data take %ss" % (t2 - t1)
  
def processData(model, input):
  """
  Process data. Bin data into options.shardCount bins. Accumulate data for each bin and populate necessary metrics. 
  """
  print 'processData data for %s' % model
  data = np.loadtxt(input, delimiter = options.delimiter,
    dtype = {'names' : ('model', 'weight', 'score', 'label'),
             'formats' : ('S16', 'f4', 'f4', 'i1')}) 
  dataSize = len(data)
  shardSize = dataSize / options.shardCount

  rocPoints = [(0, 0)]
  prPoints = []
  corrPoints = []
  cutoff = []

  totalConditionPositive = 0.0
  totalConditionNegative = 0.0

  for record in data:
    modelId = record[0]
    weight = record[1]
    score = record[2]
    label = record[3]

    if label == 1:
      totalConditionPositive += weight 
    elif label == 0:
      totalConditionNegative += weight 
    else:
      assert False, 'label invalid: %d' % label 

  truePositive = 0.0
  falsePositive = 0.0
  binTotalScore = 0.0
  binWeight = 0.0
  binPositive = 0.0
  overallTatalScore = 0.0

  partitionSize = 0
  for record in data:
    modelId = record[0]
    weight = record[1]
    score = record[2]
    label = record[3]

    partitionSize += 1
    binWeight += weight
    overallTatalScore += weight * score

    if label == 1:
      truePositive += weight
      binPositive += weight
      binTotalScore += score * weight
    elif label == 0:
      falsePositive += weight

    if partitionSize % shardSize == 0 or partitionSize == dataSize:
      recall = truePositive / totalConditionPositive
      fallout = falsePositive / totalConditionNegative;
      precision = truePositive / (truePositive + falsePositive)

      meanPctr = binTotalScore / binWeight
      eCtr = binPositive / binWeight

      rocPoints += [(fallout, recall)]
      prPoints += [(recall, precision)]
      corrPoints += [(eCtr, meanPctr)]
      cutoff += [(score, recall, fallout)]

      binWeight = 0.0
      binTotalScore = 0.0
      binPositive = 0.0

  rocPoints = sorted(rocPoints, key=lambda x:x[0])
  prPoints = sorted(prPoints, key=lambda x:x[0])
  corrPoints = sorted(corrPoints, key=lambda x:x[0])
  cutoff = sorted(cutoff, key=lambda x:x[0])

  AUC = calculateAUC(rocPoints)
  OER = truePositive / overallTatalScore  #Observed Expected Ratio
  F1 = 2 * truePositive / (truePositive + falsePositive + totalConditionPositive)

  print '%s AUC: %f' % (model, AUC)
  print '%s F1: %f' % (model, F1)
  print '%s Observed/Expected Ratio: %f' % (model, OER)
  if options.cutoff:
    print '%s cutoff:' % model, cutoff

  return model, { 'ROC': rocPoints, 'PR': prPoints, 'CORR': corrPoints, 'AUC': AUC, 'OER': OER, 'F1': F1, 'cutoff': cutoff}

def configChart():
  cf = pylab.gcf()
  defaultSize = cf.get_size_inches()
  plotSizeXRate = options.plotSizeRate
  plotSizeYRate = options.plotSizeRate
  cf.set_size_inches( (defaultSize[0]*plotSizeXRate, defaultSize[1]*plotSizeYRate) )


def main(inputDir, phrase):
  if phrase == PHRASE_GROUP:
    fileByModel = groupDataByModel(inputDir)
    if options.verbose:
      print fileByModel
    phrase = PHRASE_GROUP + 1
  else:
    fileByModel = loadFileNameByModel(MERGE_DIR)

  if phrase == PHRASE_SORT:
    sortDataFileByModel(fileByModel)
    phrase = PHRASE_SORT + 1
  else:
    fileByModel = loadFileNameByModel(SORT_DIR)

  processDataByModel(fileByModel)

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser()

  parser.add_option('-p', '--phrase', dest='phrase', default=0, type='int',
    help='Start phrase. 0:Group, 1:Sort, 2:Process')

  parser.add_option('-d', '--delimiter', dest='delimiter', default='\t',
    help='CSV field delimiter.')

  parser.add_option('-s', '--shard', dest='shardCount', default=64, type='int',
    help='Shard count. Specify how many data point to generate for plotting.')

  parser.add_option('-b', '--buffer', dest='bufferSize', default=32000, type='int',
    help='bufferSize to use for sorting')

  parser.add_option('-v', '--verbose', action='store_true', help='Be verbose')

  parser.add_option('--cutoff', dest='cutoff', action='store_true', help='print cutoff')

  parser.add_option('-i', '--ignoreInvalid', action='store_true', help='Ignore invalid in thread')

  parser.add_option('-r', '--rate', type='float', dest='plotSizeRate', default=1.5, help='Chart size rate.')

  parser.add_option('-g', '--gthumbOff', dest='gthumbOff', action='store_true', help='Don\'t open result png file.')

  parser.add_option('--mask', dest='useMask', default='', help='mask certain data. Ex \'metric_nus*,metric_supply*\'. Will remove data collection label start with \'metric_nus and metric_supply\'')

  parser.add_option('--aucSelect', dest='aucSelect', action='store_true', help='Select top n=selectLimit roc curve by roc AUC')
  parser.add_option('--selectLimit', dest='selectLimit', default=0, type='int', help='Select top n model')

  (options,args) = parser.parse_args()
  print options
  print args

  if len(args) < 1:
    print 'roc.py inputDir'
    print 'Input format: CSV by --delimiter: len(rocord)==4. Ex: modelId, weight, score, label'
    parser.print_help()
    exit()

  main(args[0], options.phrase)