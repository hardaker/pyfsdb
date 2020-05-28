#!/usr/bin/python3

"""Converts an FSDB file to a stream of json dictionaries."""

import sys
import argparse
import json
import pyfsdb

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file (FSDB file) to read")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output file (json file) to write back out")

    args = parser.parse_args()
    return args

def fsdb_to_json(input_file, output_file):
    "Converts an FSDB file to a stream of json dictionary records"
    in_fsdb = pyfsdb.Fsdb(file_handle=input_file,
                          return_type=pyfsdb.RETURN_AS_DICTIONARY)
    for record in in_fsdb:
        output_file.write(json.dumps(record) + "\n")

def main():
    "CLI wrapper around fsdb_to_json"
    args = parse_args()
    fsdb_to_json(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
