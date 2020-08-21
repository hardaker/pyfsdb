#!/usr/bin/python3

"""Converts a JSON file containing either an array of dictionaries or
individual  dictionary lines into an FSDB file"""

import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import json
import pyfsdb

def parse_args():
    """Parse command line arguments"""
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__)

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file (json file) to read")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output file (FSDB file) to write back out")

    args = parser.parse_args()
    return args

def handle_rows(out_fsdb, rows, columns):
    "Output each row in an array to the output fsdb file"
    for row in rows:
        out = []
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

    try:
        rows = json.loads(first_line)
        if not isinstance(rows, list):
            rows = [rows]
    except Exception as exp:
        sys.stderr.write("failed to parse the first line as json:\n")
        sys.stderr.write(first_line)
        sys.stderr.write(str(exp))
        sys.exit(1)

    columns = sorted(list(rows[0].keys()))
    out_fsdb = pyfsdb.Fsdb(out_file_handle=output_file)
    out_fsdb.out_column_names = columns
    handle_rows(out_fsdb, rows, columns)

    for line in input_file:
        try:
            rows = json.loads(line)
            if not isinstance(rows, list):
                rows = [rows]
            handle_rows(out_fsdb, rows, columns)
        except Exception as exp:
            sys.stderr.write("failed to parse: " + line)

def main():
    "CLI wrapper around json_to_fsdb"
    args = parse_args()
    json_to_fsdb(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
