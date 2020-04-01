#!/usr/bin/python3

"""Converts a JSON file containing either an array of dictionaries or
individual  dictionary lines into an FSDB file"""

import sys
import argparse
import json
import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file (json file) to read")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output file (FSDB file) to write back out")

    args = parser.parse_args()
    return args

def handle_rows(out_fsdb, rows):
    for row in rows:
        out_fsdb.append(list(row.values()))

def json_to_fsdb(input_file, output_file):
    first_line = next(input_file)

    rows = json.loads(first_line)
    if type(rows) is not list:
        rows = [rows]

    out_fsdb = pyfsdb.Fsdb(out_file_handle = output_file)
    out_fsdb.out_column_names = list(rows[0].keys())
    handle_rows(out_fsdb, rows)

    for line in input_file:
        rows = json.loads(line)
        if type(rows) is not list:
            rows = [rows]
        handle_rows(out_fsdb, rows)

def main():
    args = parse_args()
    json_to_fsdb(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
