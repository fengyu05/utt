#!/usr/bin/python
"""
Copy file to gateway
"""
__author__ = "zhdeng"

import sys, os, time, datetime, glob, uuid, io, random, getpass


REMOTE_FILE_CACHE_PATH = "~/.copy_to_gateway_file_cache"

options = dict()

ENV_CANASTA = "canasta"
ENV_NERTZ = "nertz"
ENV_HOLDEM = "holdem"
ENV_WAR = "war"

HOST = {
    ENV_CANASTA: "eat1-canastagw01.grid.linkedin.com",
    ENV_NERTZ: "eat1-nertzgw01.grid.linkedin.com",
    ENV_HOLDEM: "ltx1-holdemgw01.grid.linkedin.com",
    ENV_WAR: "lva1-wargw01.grid.linkedin.com",
}

DEFAULT_OUTPATH = os.environ["HOME"] + "/incoming"


def printRun(cmd):
    print cmd
    assert os.system(cmd) == 0


def main(localPath, hdfsPath):
    env = options.env
    if env not in HOST:
        print "Noknown host env  %s" % env
        exit(1)
    host = HOST[env]
    username = getpass.getuser()
    basename = os.path.basename(localPath)
    baseNameHdfs = os.path.dirname(hdfsPath)

    cmd0 = 'ssh -q -K -tt %s "rm -rf %s;mkdir %s"' % (
        host,
        REMOTE_FILE_CACHE_PATH,
        REMOTE_FILE_CACHE_PATH,
    )
    cmd1 = "scp -r %s %s@%s:%s/" % (localPath, username, host, REMOTE_FILE_CACHE_PATH)

    hadoop_cmd = "hadoop fs -mkdir -p %s;hadoop fs -copyFromLocal %s/%s %s" % (
        baseNameHdfs,
        REMOTE_FILE_CACHE_PATH,
        basename,
        hdfsPath,
    )
    if options.overwrite:
        hadoop_cmd = "hadoop fs -rmr %s;" % hdfsPath + hadoop_cmd

    cmd2 = 'ssh -q -K -tt %s "%s"' % (host, hadoop_cmd)

    printRun(cmd0)
    printRun(cmd1)
    printRun(cmd2)


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("--env", dest="env", default=ENV_HOLDEM, help="Env")
    parser.add_option("--overwrite", action="store_true", help="Override")

    (options, args) = parser.parse_args()
    print options, args
    if len(args) != 2:
        print "copy_to_gateway.py localPath hdfsPath"
        parser.print_help()
        exit()

    main(args[0], args[1])
