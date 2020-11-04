#!/usr/bin/python
import os, time, datetime, uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

options = dict()

TMP_PATH = "/tmp/.mail_chart/"


def genTodayDate():
    return datetime.datetime.today().strftime("%Y/%m/%d")


MAIL_SENDER = "hadoop.no.reply@linkedin.com"
LINKEDIN_MAIL_POSTFIX = "@linkedin.com"


def encodeDataUrl(stream):
    return stream.encode("base64").replace("\n", "")


def makeDataUrl(imageName):
    image = open(imageName, "rb")
    dataUrl = "data:image/png;base64," + encodeDataUrl(image.read())
    return dataUrl


def makeImageMIME(imagePath):
    basename = os.path.basename(imagePath)
    image = open(imagePath, "rb")
    imageMIME = MIMEImage(image.read())
    imageMIME.add_header("Content-Disposition", 'attachment; filename="%s"' % basename)
    imageMIME.add_header("Content-Id", basename)
    return imageMIME


def find_files(directory, pattern):
    import fnmatch

    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def locateCharts(options):
    files = [x for x in find_files(options.temp, "*.png")]
    return files


def sendReportMail(options, args):
    dateStr = time.strftime("%m-%d %Y")
    subject = "Hadoop charter [%s]" % dateStr
    sender = MAIL_SENDER

    receivers = options.target.split(",")
    receivers = [
        x.endswith(LINKEDIN_MAIL_POSTFIX) and x or x + LINKEDIN_MAIL_POSTFIX
        for x in receivers
    ]

    smtp = smtplib.SMTP("email.corp.linkedin.com")

    mail = MIMEMultipart()
    mail["Subject"] = subject
    mail["To"] = ",".join(receivers)

    html = "<html><head></head><body><p><h2>{0}</h2><br/>".format(subject)

    imagesList = locateCharts(options)

    for image in imagesList:
        html += '<div><img src="cid:%s" /></div>' % os.path.basename(image)

    html += "</p></body></html>"

    htmlContent = MIMEText(html, "html")
    mail.attach(htmlContent)

    for image in imagesList:
        imageMIME = makeImageMIME(image)
        mail.attach(imageMIME)

    smtp.sendmail(sender, receivers, mail.as_string())


def runCommand(command):
    print command
    assert os.system(command) == 0


def loadData(options, args):
    cmd = "rm -rf %s ; copy_from_gateway.py %s -o %s" % (
        options.temp,
        args[0],
        options.temp,
    )
    runCommand(cmd)


def main():
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("--env", default="nertz", help="env")
    parser.add_option("--temp", default=TMP_PATH, help="temp dir")
    parser.add_option("--title", default="Hadoop charter", help="title")
    parser.add_option("--target", default="zhdeng", help="target")
    (options, args) = parser.parse_args()
    print options, args

    loadData(options, args)
    sendReportMail(options, args)


if __name__ == "__main__":
    main()
