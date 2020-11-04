#!/usr/bin/python
""" Java import fixer [Productivity Tool]
Dedup and sort java import.
"""
import sys
import os
import uuid


def importNameSpacePrefix(line):
    if line.startswith("import "):
        line.replace("import ", "")

    if line.startswith("static "):
        line.replace("sstatic ", "")
    return line.split(".")[0]


def main(argv):
    if len(argv) < 2:
        print "%s filename" % argv[0]
        return
    fileName = argv[1]
    preLines = []
    importLines = []
    packageLines = []
    postLines = []

    found = False

    with open(fileName, "r") as f:
        for line in f:
            if line.startswith("import "):
                importLines.append(line)
                found = True
            elif line.startswith("package "):
                packageLines.append(line)
                found = True
            else:
                if found:
                    postLines.append(line)
                else:
                    preLines.append(line)

    packageLines = list(set(packageLines))  # unique lines
    importLines = list(set(importLines))  # unique lines

    packageLines.sort()
    importLines.sort()

    # new new line seporator
    newImportLines = []
    for line in importLines:
        if len(newImportLines) > 0 and importNameSpacePrefix(
            line
        ) != importNameSpacePrefix(newImportLines[-1]):
            newImportLines.append("\n")
        newImportLines.append(line)

    importLines = newImportLines

    print "After sort -------------------------------------------------"
    print "".join(packageLines + ["\n"] + importLines)
    print "Result end -------------------------------------------------"

    # remove ending empty preline
    filteredPreLines = []
    found = False
    preLines.reverse()
    for line in preLines:
        if not found and line == "\n":
            continue
        else:
            found = False
            filteredPreLines.append(line)
    filteredPreLines.reverse()

    # remove pending empty postline
    filteredPostLines = []
    found = False
    for line in postLines:
        if not found and line == "\n":
            continue
        else:
            found = True
            filteredPostLines.append(line)

    lines = (
        filteredPreLines
        + packageLines
        + ["\n"]
        + importLines
        + ["\n"]
        + filteredPostLines
    )

    homeDir = os.environ["HOME"]
    backupFileName = str(uuid.uuid4())
    backupPath = homeDir + "/.backup/" + backupFileName
    print "Backup Path:", backupPath
    os.system("mkdir -p " + homeDir + "/.backup")
    os.system("cp " + fileName + " " + backupPath)

    with open(fileName, "w") as f:
        f.writelines(lines)
        f.close()


if __name__ == "__main__":
    main(sys.argv)
