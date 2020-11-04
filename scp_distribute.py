#!/usr/bin/python

"""
Distribute file via scp
scp_distribute from/to/edit path
"""
import os, time, sys, socket, getpass

HOME_PATH = os.environ["HOME"]
INCOMING = HOME_PATH + "/incoming/"
TARGET_INCOMING = "~/incoming/"
DISTRIBUTE_LIST = HOME_PATH + "/.scp_distribute_list"
CMD_FILE = HOME_PATH + "/.scp"

USERNAME = getpass.getuser()

COPY_TO_ALIAS = "#!/bin/bash\n~/.scp to $*"
COPY_FROM_ALIAS = "#!/bin/bash\n~/.scp from $*"

USAGE = {
    "to": "copy_to host files...",
    "from": "copy_from host files...",
}

_networkLoaded = False


def makeAlias():
    printRun("mkdir -p ~/bin")
    printRun("echo '%s' > ~/bin/copy_to" % COPY_TO_ALIAS)
    printRun("echo '%s' > ~/bin/copy_from" % COPY_FROM_ALIAS)
    printRun("chmod a+x ~/bin/copy_to")
    printRun("chmod a+x ~/bin/copy_from")


def printRun(cmd, skipAssert=False):
    print cmd
    if not skipAssert:
        assert os.system(cmd) == 0


def prepare(thisCmd):
    print "Init ..."
    printRun("mkdir -p %s" % INCOMING)
    printRun("diff %s %s || cp %s %s" % (CMD_FILE, thisCmd, thisCmd, CMD_FILE))
    makeAlias()


def editList():
    printRun("vim %s" % DISTRIBUTE_LIST)


def loadHostTable():
    hostTable = {}
    if not os.path.exists(DISTRIBUTE_LIST):
        print "can't sync because of lack of distribute list"
        exit(1)
    for line in open(DISTRIBUTE_LIST).readlines():
        if not line.strip():
            continue
        fileds = line.split(" ")
        assert len(fileds) == 2
        host = fileds[0].strip()
        name = fileds[1].strip()
        ip = ""
        try:
            ip = socket.gethostbyname(name)
        except:
            try:
                ip = socket.gethostbyname(socket.gethostbyaddr(name)[0])
            except:
                pass

        if not ip:
            print "cant't resovled %s" % name
            continue

        hostTable[host] = {"name": name, "ip": ip}
    return hostTable


def getLocalHost():
    return socket.gethostbyname(socket.gethostname())


def sync():
    loadNetwork()
    for (host, hostRecord) in hostTable.iteritems():
        name = hostRecord["name"]
        ip = hostRecord["ip"]

        if ip not in localHost:
            print "Sync to %s[%s]" % (name, ip)
            try:
                copyTo(host, [DISTRIBUTE_LIST, CMD_FILE], "~/")
            except:
                print "Scp failed on %s" % name
        else:
            print "skip %s" % ip


def copyTo(host, files, target, initTarget=False):
    loadNetwork()
    if host not in hostTable:
        print "%s not exist in host list" % host
        exit(1)
    ip = hostTable[host]["ip"]
    if initTarget:
        printRun('ssh %s@%s "mkdir -p %s"' % (USERNAME, ip, target))
    printRun("scp -r %s %s@%s:%s" % (" ".join(files), USERNAME, ip, target))


def copyFrom(host, files, target):
    loadNetwork()
    if host not in hostTable:
        print "%s not exist in host list" % host
        exit(1)
    ip = hostTable[host]["ip"]
    joinedList = ""
    if len(files) > 1:
        joinedList = "\{%s\}" % ",".join(files)
    else:
        joinedList = files[0]

    printRun("scp -r %s@%s:%s %s" % (USERNAME, ip, joinedList, target))


def usage(mode):
    print USAGE[mode]
    exit(1)


def loadNetwork():
    global _networkLoaded
    if _networkLoaded:
        return
    global hostTable
    hostTable = loadHostTable()
    print "HostTable:", hostTable
    global localHost
    localHost = getLocalHost()
    print "localHost:", localHost
    _networkLoaded = True


def main(argv):
    mode = argv[1]
    if mode == "from":
        if len(argv) < 4:
            usage(mode)
        copyFrom(argv[2], argv[3:], INCOMING)
    elif mode == "to":
        if len(argv) < 4:
            usage(mode)
        copyTo(argv[2], argv[3:], TARGET_INCOMING, True)
    elif mode == "edit" or mode == "list":
        editList()
    elif mode == "sync":
        prepare(argv[0])
        sync()
    elif mode == "init":
        prepare(argv[0])


if __name__ == "__main__":
    main(sys.argv)
