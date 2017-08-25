#!/usr/bin/python
import os
import urllib

CURLI = '/usr/local/linkedin/bin/curli'
D2_PREFIX = 'd2://'
X_POST = ' -X POST'

CURLI_PARAMETERS = [
    'pretty-print'
  ]

ENV_DEV = 'dev'
ENV_PROD = 'prod'

def doubleQuote(msg):
  return '"' + msg + '"'

def singleQuote(msg):
  return "'" + msg + "'"

def makeDataList(data):
  text = '['
  isFirst = True
  for v in data:
    if not isFirst:
      text += ','
    if type(v) == str or type(v) == unicode:
      text += doubleQuote(v)
    elif type(v) == int or type(v) == long:
      text += str(v)
    elif type(v) == bool:
      text += v and 'true' or 'false'
    elif type(v) == dict:
      text += makeDataDict(v)
    elif type(v) == list:
      text += makeDataList(v)
    isFirst = False

  text += ']'
  return text

def makeDataDict(data):
  text = '{'

  isFirst = True
  for k, v in data.iteritems():
    if not isFirst:
      text += ','
    text += doubleQuote(k) + ':'
    if type(v) == str or type(v) == unicode:
      text += doubleQuote(v)
    elif type(v) == int or type(v) == long:
      text += str(v)
    elif type(v) == bool:
      text += v and 'true' or 'false'
    elif type(v) == dict:
      text += makeDataDict(v)
    elif type(v) == list:
      text += makeDataList(v)

    isFirst = False

  text += '}'
  return text

def makeArgStringV1(data):
  result = ''
  isFirst = True
  for k, v in data.iteritems():
    if not isFirst:
      result += '&'
    else:
      isFirst = False
    result += k + '=' + v
  return result

def makeArgV2(v):
  if type(v) == str or type(v) == unicode:
    return urllib.quote(v)
  elif type(v) == int or type(v) == long:
    return str(v)
  elif type(v) == bool:
    return 'true' if v else 'false'
  elif type(v) == dict:
    result = '('
    isFirst = True
    for kk, vv in v.iteritems():
      if not isFirst:
        result += ','
      result += '%s:' % kk
      result += makeArgV2(vv)
      isFirst = False
    result += ')'
    return result
  elif type(v) == list:
    result = 'List('
    isFirst = True
    for vv in v:
      if not isFirst:
        result += ','
      result += makeArgV2(vv)
      isFirst = False
    result += ')'
    return result


  assert False, 'unkown value type in v2:' + type(v)


def makeArgStringV2(data):
  result = ''
  first = True
  for k, v in data.iteritems():
    if not first:
      result += '&'
    else:
      first = False
    result += k + '=' + makeArgV2(v)
  return result

class Request(object):

  def __init__(self, env=ENV_DEV, headers=[], user=None, password=None,
      localResource=None, concurrent=None, describe=None, restMethod=None, V2=False):
    self.env = env
    self.headers = headers
    self.user = user
    self.password = password
    self.localResource = localResource
    self.concurrent = concurrent
    self.describe = describe
    self.restMethod = restMethod
    self.V2 = V2

  def setEnv(self, env):
    self.env = env

  def addHeader(self, header):
    self.headers.append(header)

  def addUser(self, user):
    self.user = user

  def addPassword(self, password):
    self.password = password

  def makeParametersSection(self):
    result = ''
    for parameter in CURLI_PARAMETERS:
      result += ' --' + parameter
    if self.env.startswith(ENV_PROD):
      result += ' --fabric=%s' % self.env

    return result

  def isProdEnv(self):
    return self.env.startswith(ENV_PROD)

  def setConcurrent(self, concurrent):
    self.concurrent = concurrent

  def isV2(self):
    return self.V2

  def enableV2(self):
    self.V2 = True

  def execute(self):
    if self.isProdEnv():
      cmd = 'ssh -q -K -tt %s "%s"' % ('eng-portal', self.getCurli())
    else:
      if self.concurrent:
        cmd = self.getCurli() + '&'
      else:
        cmd = self.getCurli()
    print cmd
    os.system(cmd)

  def getEnv(self):
    return self.env

  def makeDataSection(self):
    if type(self.data) is dict:
      return ' --data \'' + makeDataDict(self.data) + '\''
    else:
      return ''

  def makeUrlParamerters(self):
    if not type(self.urlParam) is dict:
      return ''
    params = ['%s=%s' %(k, urllib.quote(v)) for (k, v) in self.urlParam.iteritems()]
    return '&'.join(params)

  def makeHeaderSection(self):
    result = ''
    for header in self.headers:
      result += ' -H \'%s\'' % header

    if self.restMethod:
      result += ' -H X-RestLi-Method:%s' % self.restMethod

    if self.V2:
      result += ' -H \'X-RestLi-Protocol-Version: 2.0.0\''

    if self.user:
      result += ' --user %s' % self.user

    if self.password:
      result += ' --password %s' % self.password

    if self.describe:
      result += ' -D -'


    return result

  def getResourcePrefix(self):
    if self.localResource:
      return self.localResource
    else:
      return D2_PREFIX + self.resource

  def setLocalResource(self, localResource):
    self.localResource = localResource

'''
GET REQUEST
'''
class GetRequest(Request):
  '''
  GetRequest -> Request
  1) Get id: 'd2://resource/id' -X GET'
  2) Get urlParam: 'd2://resource/{urlParam flatten}' -X GET'
  '''
  def __init__(self, resource, id=None, urlParam=None, data=None, X='GET'):
    super(GetRequest, self).__init__(describe=True)
    self.resource = resource
    self.id = id
    self.urlParam = urlParam
    self.data = data
    self.X = X

  def getResource(self):
    if self.id:
      return singleQuote(self.getResourcePrefix() + '/' + str(self.id))
    elif self.urlParam:
      return singleQuote(self.getResourcePrefix() + '/' + self.makeUrlParamerters())
    else:
      return singleQuote(self.getResourcePrefix())

  def getCurli(self):
    return CURLI + self.makeParametersSection() + ' ' \
        + self.getResource() + " -X %s" % self.X\
        + self.makeHeaderSection() \
        + self.makeDataSection()

class PutRequest(GetRequest):
  '''
  PutRequest -> GetRequest -> Request
  1) Put id: 'd2://resource/id' -X PUT --data '{...}'
  2) Put urlParam: 'd2://resource/{urlParam flatten}' -X PUT --data '{}'
  '''
  def __init__(self, resource, id=None, urlParam=None, data=None):
    super(GetRequest, self).__init__(describe=True)
    self.resource = resource
    self.id = id
    self.urlParam = urlParam
    self.data = data
    if self.data is None:
      self.data = {}
    self.X = 'PUT'

class DeleteRequest(GetRequest):
  def __init__(self, resource, id=None, urlParam=None):
    super(GetRequest, self).__init__(describe=True)
    self.resource = resource
    self.id = id
    self.urlParam = urlParam
    self.data = data
    if self.data is None:
      self.data = {}
    self.X = 'DELETE'

'''
End of GET/PUT/DELETE
'''

class FinderRequest(Request):
  '''
  FinderRequest -> GetRequest -> Request
  1) Get without finder name: 'd2://resource?a=x&b=y&c=z' -X GET
  1) Get with finder name: 'd2://resource?q=finderName&a=x&b=y&c=z' -X GET
  '''
  def __init__(self, resource, finderName, data):
    super(FinderRequest, self).__init__(describe=True)
    self.resource = resource
    self.finderName = finderName
    self.data = data
    if finderName:
      self.data['q'] = finderName

  def getResource(self):
    return singleQuote(self.getResourcePrefix() + '?' + self.makeArgsSection())

  def makeArgsSection(self):
    if self.isV2():
      return makeArgStringV2(self.data)
    else:
      return makeArgStringV1(self.data)

  def getCurli(self):
    return CURLI + self.makeParametersSection() + ' ' \
        + self.getResource() + " -X GET " \
        + self.makeHeaderSection()

class FacetFinderRequest(FinderRequest):
  def __init__(self, resource, finderName, data, sortData=None, pageData=None):
    super(FacetFinderRequest, self).__init__(resource, finderName, data)
    self.sortData = sortData
    self.pageData = pageData

  def makeArgsSection(self):
    return self.makeFacetSection(self.data) + self.makeSortSection(self.sortData) + self.makePageSection(self.pageData) + self.makeFields()

  def makeFacetSection(self, data):
    result = ""
    for k, v in data.iteritems():
      result += '&facet=' + k + ',' + str(v)

    return result

  def setFields(self, fields):
    self.fields = fields

  def makeSortSection(self, sortData):
    if not sortData:
      return ""
    result = ""
    for v in sortData:
      result += '&sort=' + str(v)
    return result

  def makePageSection(self, pageData):
    if not pageData:
      return ""
    result = ""
    result += '&paging.count=' + str(pageData['count'])
    return result

  def makeFields(self):
    try:
      return '&fields=%s' % ','.join(self.fields)
    except:
      return ''


class PostRequest(Request):
  def __init__(self, resource, method, data, id=None):
    super(PostRequest, self).__init__(describe=True, restMethod=method)
    self.resource = resource
    self.method = method
    self.data = data
    if id:
      self.id = id
    else:
      self.id = None

  def setId(self, id):
    self.id = id

  def getResource(self):
    if self.id:
      return singleQuote(self.getResourcePrefix() + '/' + str(self.id))
    else:
      return singleQuote(self.getResourcePrefix())

  def getCurli(self):
    return CURLI + self.makeParametersSection() + ' ' + self.getResource() + X_POST + self.makeHeaderSection() + self.makeDataSection()

class ActionRequest(Request):
  def __init__(self, resource, action, data):
    super(ActionRequest, self).__init__()
    self.resource = resource
    self.action = action
    self.data = data

  def getResource(self):
    return singleQuote(self.getResourcePrefix() + '?action=%s' % self.action)

  def makeHeaderSection(self):
    header = super(ActionRequest, self).makeHeaderSection()
    return header + ' -D - '

  def getCurli(self):
    return CURLI + self.makeParametersSection() + ' ' + self.getResource() + X_POST + self.makeHeaderSection() + self.makeDataSection()

