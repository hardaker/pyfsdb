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
    parser = argparse.ArgumentParser(
        formatter_class=formatter_class, description=__doc__
    )

    parser.add_argument(
        "-t",
        "--type-list",
        default=[],
        type=str,
        nargs="*",
        help="A list of column=type values, where type can be 'd' (float) or 'l' (integer)",
    )

    parser.add_argument(
        "-a",
        "--auto-types",
        action="store_true",
        help="Guess at type values based on the first row",
    )

    parser.add_argument(
        "input_file", type=argparse.FileType("r"), nargs="?", default=sys.stdin, help=""
    )

    parser.add_argument(
        "output_file",
        type=argparse.FileType("w"),
        nargs="?",
        default=sys.stdout,
        help="",
    )

    args = parser.parse_args()
    return args


def add_types(input_file, output_file, types=[], auto_convert=False):
    # we do this without using an FSDB class, since raw I/O is faster
    fsdb_line = next(input_file)
    first_line = next(input_file)
    buffer = io.StringIO(fsdb_line + first_line)

    fh = pyfsdb.Fsdb(file_handle=buffer, return_type=pyfsdb.RETURN_AS_DICTIONARY)
    columns = fh.column_names

    converters = fh.converters

    # if auto_conversion, then make some guesses
    if auto_convert:
        first_row = next(fh)
        converters = fh.guess_converters(first_row)

    if not converters:
        converters = {}

    # specifications should override autos
    for specification in types:
        (column, dtype) = specification.split("=")
        if column not in columns:
            raise ValueError(f"Invalid column: {column} in '{specification}")
        converters[column] = pyfsdb.fsdb.incoming_type_converters[dtype]

    # create the new header line with conversions in place
    fh.converters = converters
    new_header = fh.create_header_line(separator_token=fh.separator_token)

    output_file.write(new_header)
    output_file.write(first_line)

    # read the rest as chunks
    while True:
        data = input_file.read(1024 * 1024 * 1024)  # 1M at a time
        if not data:
            break
        output_file.write(data)


def main():
    args = parse_args()

    add_types(args.input_file, args.output_file, args.type_list, args.auto_types)


if __name__ == "__main__":
    main()
