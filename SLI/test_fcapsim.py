#!/usr/bin/python
# unit tests for fcap simulation uttility.
# go/fcapsim

import math
from fcapsim import *

EPS = 1E-7

def fequals(a, b):
  return abs(a - b) < EPS

def test_CDF_byLambdaSeries():
  lambdaSeries = [0.5,0.5,0.5,0.7,0.9,1.1,1.1] #len = 7

  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 0)) , 0)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 0.5)) ,0.5)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 1.5)) , 1.5)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 2.5)) , 2.5)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 3.5)) , 3.5)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 4.5)) , 4.5)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 5.5)) , 5.5)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 6.5)) , 6.5)
  assert fequals(inverseCDF_byLambdaSeries(lambdaSeries, CDF_byLambdaSeries(lambdaSeries, 7.0)) , 7.0)


def test_GenerateDeltaTimeWithinPeriod():
  lambdaSeries = [0.5,0.5,0.5,0.7,0.9,1.1,1.1] #len = 7
  seq = generateDeltaTimeWithinPeriod(lambdaSeries * 4, 28.0)
  assert len(seq) > 0 # seq will never be empty
  assert len([ x for x in seq if x > 28.0]) == 0 #seq will never fall outside

def test_RestoreLambdaTsFromPvTs():
  lambdaTs = restoreLambdaTsFromPvTs([3,2,1,2,2], 0.5)
  assert lambdaTs == [0.33333333333333331, 0.5, 1.0, 0.5, 0.5]

