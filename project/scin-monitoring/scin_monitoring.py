#!/usr/bin/python
import os, time, datetime, uuid
import smtplib
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

options = dict()
HADOOP_DATA_PATH = '/jobs/fcst/scin/monitoring/'

PICTURE_PATH = './results/'
DATA_PATH = './data/'

ALL_HADOOP_DATA_FILE = [
  'base_profile',
  'channel_breakdown',
  'validation_error_rate'
  ]

ALL_PICTURE = ['channel_breakdown.png',
       'base_profile.png',
       'validation_error_rate.png'
  ]

ALL_PLOT_CMD = [
  './plot_chart.py --folder data/base_profile --chart trend --dateM -o base_profile -l -t "BaseProfileHistroy all dimension" -y Impression -r 1.5',
  './plot_chart.py --folder data/channel_breakdown --chart trend --dateM -o channel_breakdown -t "Channel breakdown" -y Impression -r 1.5',
  './plot_chart.py --folder data/validation_error_rate --chart scatter --dateX -o validation_error_rate -t "Error rate" -y Rate -r 1.5'
  ]

MAIL_SENDER = 'forecast.noreply@linkedin.com' 

DEBUG_ALL_RECIEVER = ['zhdeng@linkedin.com']

DEV_ALL_RECIEVER = ['zhdeng@linkedin.com', 'dawang@linkedin.com', 'syou@linkedin.com']

ALL_RECIEVER = ['eng.ms.as.dev@linkedin.com']

def encodeDataUrl(stream):
  return stream.encode('base64').replace('\n', '')

def makeDataUrl(imageName):
  image = open(imageName, 'rb')
  dataUrl = 'data:image/png;base64,'+encodeDataUrl(image.read())
  return dataUrl

def makeImageMIME(imagePath):
  basename = os.path.basename(imagePath)
  image = open(imagePath, 'rb')
  imageMIME = MIMEImage(image.read())
  imageMIME.add_header('Content-Disposition', 'attachment; filename="%s"' % basename) 
  imageMIME.add_header('Content-Id', basename) 
  return imageMIME


def sendReportMail(sender, receivers, subject, imagesList):
  dateStr = time.strftime('%m-%d %Y')
  smtp = smtplib.SMTP('email.corp.linkedin.com')

  mail = MIMEMultipart()
  mail['Subject'] = subject
  mail['To'] = ','.join(receivers)

  html = """\
          <html>
          <head></head>
          <body>
          <p><h2>SCIN forecast monitoring : %s </h2><br/>

          Monitoring UnifedImpressionEvent input, event count breakdown by channel:<br/>
          <img src="cid:%s"></img>

          Monitoring total impression of all dimension in BaseProfileHistory:<br/>
          <img src="cid:%s"></img>

          Monitoring Error rate(compute by validation) breakdown by metric:<br/>
          <img src="cid:%s"></img>

          To ignore this mail, please filter out mail sent from forecast.noreply@linkedin.com<br/>
          Support zhdeng@linkedin.com<br/> 
          </p>
          </body>
          </html>
  """ %(dateStr, imagesList[0], imagesList[1], imagesList[2])

  htmlContent = MIMEText(html, 'html')
  mail.attach(htmlContent)

  for imagePath in imagesList:
    imageMIME = makeImageMIME(PICTURE_PATH + imagePath)
    mail.attach(imageMIME)

  smtp.sendmail(sender, receivers, mail.as_string()) 

def ensureDir(dirName):
  """
  Create directory if necessary.
  """
  if not os.path.exists(dirName):
    os.makedirs(dirName)

def prepareDir():
  ensureDir(PICTURE_PATH)
  ensureDir(DATA_PATH)

def runCommand(command):
  print command
  assert os.system(command) == 0

def copyData():
  for hadoopFile in ALL_HADOOP_DATA_FILE:
    hadoopFilePath = HADOOP_DATA_PATH + hadoopFile + '/*'
    localFilePath = DATA_PATH + hadoopFile
    print 'Copy %s' % hadoopFilePath

    remoteCommand = '"rm -rf ~/.magic_file_cache;mkdir -p ~/.magic_file_cache/%s;' % hadoopFile +\
      'hadoop fs -copyToLocal %s ~/.magic_file_cache/%s/;' % (hadoopFilePath, hadoopFile) +\
      'copy_to_home ~/.magic_file_cache/%s"' % hadoopFile
    sshCommand = 'ssh -q -K -tt eat1-magicgw01.grid.linkedin.com %s' % remoteCommand
    mvCommand = 'rm -rf %s;mv ~/incoming/%s %s' %(localFilePath, hadoopFile, DATA_PATH)

    runCommand(sshCommand)
    runCommand(mvCommand)

  for hadoopFile in ALL_HADOOP_DATA_FILE:
    assert os.path.exists(DATA_PATH + hadoopFile) == 1, '%s not exist' % hadoopFile

def plotData():
  for cmd in ALL_PLOT_CMD:
    runCommand(cmd)

def main():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--mode', dest='mode', default='debug', help='mode')
  parser.add_option('--skip', dest='skip', default='', help='mode')
  (options,args) = parser.parse_args()

  prepareDir()
  if options.skip and options.skip == 'copy':
    pass
  else:
    copyData()

  plotData()

  if options.mode == 'prod':
    sendReportMail(MAIL_SENDER, ALL_RECIEVER, 'SCIN forecast monitoring', ALL_PICTURE)
  elif options.mode == 'dev':
    sendReportMail(MAIL_SENDER, DEV_ALL_RECIEVER, 'SCIN forecast monitoring', ALL_PICTURE)
  else:
    sendReportMail(MAIL_SENDER, DEBUG_ALL_RECIEVER, 'SCIN forecast monitoring', ALL_PICTURE)


if __name__ == '__main__':
  main()

