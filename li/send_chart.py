#!/usr/bin/python
import os, time, datetime, uuid
import smtplib
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

options = dict()

PICTURE_PATH = './results/'
EXTENTION = '.png'

def encodeDataUrl(stream):
  return stream.encode('base64').replace('\n', '')

def makeDataUrl(imageName):
  image = open(imageName, 'rb')
  dataUrl = 'data:image/png;base64,'+encodeDataUrl(image.read())
  return dataUrl

def makeImageMIME(imagePath):
  if not os.path.exists(imagePath):
    if os.path.exists(imagePath + EXTENTION):
      imagePath = imagePath + EXTENTION
    else:
      print 'Image %s not exist' % imagePath
      return None

  basename = os.path.basename(imagePath)
  image = open(imagePath, 'rb')
  imageMIME = MIMEImage(image.read())
  imageMIME.add_header('Content-Disposition', 'attachment; filename="%s"' % basename) 
  imageMIME.add_header('Content-Id', basename) 
  return imagePath, imageMIME


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
          <p><h2>Hadoop Charter : %s </h2><br/>""" % dateStr



  foundImageCount = 0
  for image in imagesList:
    print 'attach image: %s' % image
    imagePath, imageMIME = makeImageMIME(image)
    if imageMIME:
      foundImageCount += 1
      mail.attach(imageMIME)
      html += '<img src="cid:%s"></img>' % (os.path.basename(imagePath))

  htmlEnd = """</p></body></html>"""

  html += htmlEnd
  htmlContent = MIMEText(html, 'html')
  mail.attach(htmlContent)

  if foundImageCount > 0:
    smtp.sendmail(sender, receivers, mail.as_string())
  else:
    print 'No image attach, exist'
    exit(1)


def main():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-r', '--reciever', dest='reciever', default='zhdeng@linkedin.com', help='')
  parser.add_option('-s', '--sender', dest='sender', default='hd-charter-noreply@linkedin.com', help='')
  parser.add_option('-t', '--title', dest='title', default='Hadoop charter', help='')
  parser.add_option('-p', '--path', dest='path', default=PICTURE_PATH, help='')

  parser.add_option('-f', '--file', dest='file', default='', help='require')

  (options,args) = parser.parse_args()
  if (not options.file) and (not len(args) > 0):
    parser.print_help()
    exit()

  print ('Params %s' % options)
  print ('Args %s' % args)

  if options.file:
    sendReportMail(options.sender, [options.reciever], options.title, options.file.split(','))
  else:
    sendReportMail(options.sender, [options.reciever], options.title, args)

if __name__ == '__main__':
  main()

