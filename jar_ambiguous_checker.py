#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Check if there is any ambiguous class in list jar.
To prevent java.lang.NoSuchMethodError in runtinue env.
"""
__author__ = "zhdeng"
__version__ = "0.1"


import sys
import zipfile
import glob
import subprocess


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def main():
    try:
        jarMap = {}
        for arg in args:
            for file in glob.glob(arg):
                jarMap[file] = file

        jarList = [x for x in jarMap if x.endswith(".jar")]

        classMap = {}
        for jar in jarList:
            if options.report:
                print "Jar: %s" % jar

            output = subprocess.Popen(
                ["jar", "tf", jar], stdout=subprocess.PIPE
            ).communicate()[0]
            lines = output.split("\n")

            for line in lines:
                if line.endswith(".class"):
                    if options.report:
                        print line
                        continue

                    if line in classMap:
                        print "[Warning][Check Java Jar Ambiguous] %s exist in both %s and %s" % (
                            line,
                            jar,
                            classMap[line],
                        )
                    else:
                        classMap[line] = jar

    except Exception, e:
        if options.safe:
            return 0
        else:
            raise e


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option(
        "--safe", dest="safe", default=True, help="safe mode. Failed silently"
    )
    parser.add_option(
        "--report", dest="report", default=False, help="report class list"
    )

    (options, args) = parser.parse_args()
    main()
