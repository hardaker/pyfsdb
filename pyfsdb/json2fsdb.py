#!/usr/bin/python3

"""Converts a JSON file containing either an array of dictionaries or
individual  dictionary lines into an FSDB file"""

import sys
import argparse
import json
import pyfsdb

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file (json file) to read")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output file (FSDB file) to write back out")

    args = parser.parse_args()
    return args

def handle_rows(out_fsdb, rows, columns):
    "Output each row in an array to the output fsdb file"
    for row in rows:
        out=[]
        for column in columns:
            if column in row:
                out.append(row[column])
            else:
                out.append('')
        out_fsdb.append(out)

def json_to_fsdb(input_file, output_file):
    """A function that converts an input file stream of json dictionary
    to an output FSDB file, where the header column names are pulled
    from the first record keys."""
    first_line = next(input_file)

    rows = json.loads(first_line)
    if type(rows) is not list:
        rows = [rows]

    columns = sorted(list(rows[0].keys()))
    out_fsdb = pyfsdb.Fsdb(out_file_handle=output_file)
    out_fsdb.out_column_names = columns
    handle_rows(out_fsdb, rows, columns)

    for line in input_file:
        rows = json.loads(line)
        if type(rows) is not list:
            rows = [rows]
        handle_rows(out_fsdb, rows, columns)

def main():
    "CLI wrapper around json_to_fsdb"
    args = parse_args()
    json_to_fsdb(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
