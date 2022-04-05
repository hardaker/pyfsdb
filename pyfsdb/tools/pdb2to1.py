#!/usr/bin/python3

"Converts a FSDB2 (with type specifications) to an FSDB1 for use with older tools"

import sys
import os
import argparse
import collections

import pyfsdb
import re

def parse_args():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class,
                                     description=__doc__)

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # we do this without using an FSDB class, since raw I/O is faster
    fsdb_line = next(args.input_file)
    fsdb_line = re.sub(r":\w+", "", fsdb_line)
    args.output_file.write(fsdb_line)

    while (data := args.input_file.read(1024*1024*1024)):  # 1M at a time
        args.output_file.write(data)


if __name__ == "__main__":
    main()
