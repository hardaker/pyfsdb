#!/usr/bin/python3

"""Adds type hints for converting a FSDB1 format to add type hints to columns.
   This allows compliant tools to get automatic type conversion within their scripts."""

import sys
import os
import argparse
import collections

import pyfsdb
import re
import io

def parse_args():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class,
                                     description=__doc__)

    parser.add_argument("-t", "--type-list", default=[], type=str, nargs="*",
                        help="A list of column=type values, where type can be 'd' (float) or 'l' (integer)")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="")

    args = parser.parse_args()
    return args


def add_types(input_file, output_file, types):
    # we do this without using an FSDB class, since raw I/O is faster
    fsdb_line = next(input_file)
    buffer = io.StringIO(fsdb_line)

    fh = pyfsdb.Fsdb(file_handle=buffer)
    columns = fh.column_names

    converters = fh.converters
    if not converters:
        converters = {}

    for specification in types:
        (column, dtype) = specification.split("=")
        if column not in columns:
            raise ValueError(f"Invalid column: {column} in '{specification}")
        converters[column] = pyfsdb.fsdb.incoming_type_converters[dtype]

    fh.converters = converters
    new_header = fh.create_header_line(separator_token=fh.separator_token)

    output_file.write(new_header)

    # read the rest as chunks
    while (data := input_file.read(1024*1024*1024)):  # 1M at a time
        output_file.write(data)


def main():
    args = parse_args()

    add_types(args.input_file, args.output_file, args.type_list)


if __name__ == "__main__":
    main()
