#!/usr/bin/python
import json
import sys


def main(args):
    if len(args) < 2:
        print "%s filename" % args[0]
        return

    json.loads(args[1])


if __name__ == "__main__":
    main(sys.argv)
