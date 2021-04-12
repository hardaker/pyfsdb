#!/usr/bin/python3

"""dbdatetoepoch converts a unix epoch timestamp column into a human
readable date string usting strftime with an adjustable format."""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys
import pyfsdb
from dateparser import parse
import time

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
	                        epilog="Exmaple Usage: dbdatetoepoch -d human_column -t timestamp_column input.fsdb output.fsdb")

    parser.add_argument("-t", "--timestamp-column", default="timestamp",
                        type=str, help="Column to use with the epoch timestamp")

    parser.add_argument("-T", "--time-column", default="timestamp_human", type=str,
                        help="The output time/date column to create")

    parser.add_argument("-f", "--format", default="%Y-%m-%d %H:%M", type=str,
                        help="The output format to use in the time column")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    fh = pyfsdb.Fsdb(file_handle=args.input_file,
                     out_file_handle=args.output_file,
                     converters={args.timestamp_column: float})
    column_names = fh.column_names
    fh.out_column_names = column_names + [args.time_column]

    timestamp_column = fh.get_column_number(args.timestamp_column)

    colfmt = args.format

    for row in fh:
        row[-1] = time.strftime(colfmt, time.localtime(row[timestamp_column]))
        fh.append(row)


if __name__ == "__main__":
    main()
