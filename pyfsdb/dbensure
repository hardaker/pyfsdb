#!/usr/bin/python3

"""dbensure can be used that some or all fields in a table contain data.

If rows with the specified columns (default: all) don't contain data,
they're dropped from the output rows."""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys

import pyfsdb

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
	                        epilog="Exmaple Usage: dbensure input_file.fsdb output_file.fsdb")

    parser.add_argument("-c", "--columns", nargs="*",
                        help="The columns to check in the data")

    parser.add_argument("-v", "--fill", default=None, type=str,
                        help="Don't drop the rows but fill with this value if a column is missing")

    parser.add_argument("-e", "--print-error", action="store_true",
                        help="Print an error message on each dropped row")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file to process")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Where to send the output data")

    args = parser.parse_args()
    return args

def filter_row(row, columns, fill_value, print_error):
    for column in columns:
        if row[column] == "":
            if fill_value:
                row[column] = fill_value
            else:
                if print_error:
                    sys.stderr.write("# dbensure dropping row:" + str(row) + "\n")
                return
    return row

def main():
    args = parse_args()
    fh = pyfsdb.Fsdb(file_handle=args.input_file,
                     out_file_handle=args.output_file)

    if args.columns:
        column_nums = fh.get_column_numbers(args.columns)
    else:
        column_nums = list(range(len(fh.column_names)))

    fh.filter(filter_row, args=[column_nums, args.fill, args.print_error])

if __name__ == "__main__":
    main()
