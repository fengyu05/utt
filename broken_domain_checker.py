#!/usr/bin/python

"""
Check whether a domain is broken.
"""
import sys
import os
import subprocess
import httplib
import re

options = dict()
args = list()

urlPattern = r"[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*"

pattern = re.compile(urlPattern)


def isLive(url):
    if pattern.match(url):
        conn = httplib.HTTPConnection(url, 80, timeout=1)
        try:
            conn.request("HEAD", "")
            res = conn.getresponse()
            return res.status == 200
        except:
            return False
    else:
        return Fasle


def main(args):
    input = args[0]

    for line in open(input, "r").readlines():
        url = line.strip()
        if isLive(url):
            print "GOOD:", url
        else:
            print "BAD:", url


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option(
        "-o",
        "--output",
        dest="output",
        default="good_domain.txt",
        help="Good domain output",
    )

    (options, args) = parser.parse_args()

    main(args)
