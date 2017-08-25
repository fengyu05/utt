#!/bin/python
import os

#clusters = ['lca1', 'EI3', 'ltx1']
clusters = ['lca1']
for i in xrange(1):
  for cluster in clusters:
    cmd = "curl -X DELETE --header 'Accept: text/plain' 'http://%s-pinot-controller.stg.linkedin.com:11984/segments/scinForecasting/nativeAdsForecasting_nativeAdsForecasting_nativeAdsCorrelation_1_%s'" % (cluster, i)
    print cmd
    os.system(cmd)


