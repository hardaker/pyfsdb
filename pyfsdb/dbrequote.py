#!/usr/bin/python3

"""Passes the requested columns (-k) through the python regex escaping function.

Note: because -k can take multiple columns, input files likely need to appear
after the "--" argument-stop-parsing string.
"""

import pyfsdb
from re import escape

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
	                        epilog="Exmaple Usage: dbrequote -k column1 column2 -- file.fsdb")

    parser.add_argument("-k", "--keys-to-escape", type=str, nargs="+",
                        help="The keys to regexp quote")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file to parse")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Where to send the output")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    fs = pyfsdb.Fsdb(file_handle = args.input_file,
                     out_file_handle = args.output_file)

    convert_cols = fs.get_column_numbers(args.keys_to_escape)

    for row in fs:
        for column in convert_cols:
            row[column] = escape(row[column])
        fs.append(row)

if __name__ == "__main__":
    main()
