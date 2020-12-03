#!/usr/bin/python3

"""dbdatetoepoch converts a timestamp column with a human date to a
unix epoch timestamp column"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys
import pyfsdb
from dateparser import parse

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
	                        epilog="Exmaple Usage: dbdatetoepoch -d human_column -t timestamp_column input.fsdb output.fsdb")

    parser.add_argument("-d", "--date-column", default="date", type=str,
                        help="Date column to use")

    parser.add_argument("-t", "--timestamp-column", default="timestamp", type=str,
                        help="Column to create for storing an epoch column")

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
                     out_file_handle=args.output_file)
    column_names = fh.column_names
    fh.out_column_names = column_names + [args.timestamp_column]

    date_column = fh.get_column_number(args.date_column)
    for row in fh:
        timestamp_value = 0
        try:
            timestamp_value = parse(row[date_column]).timestamp()
        except Exception:
            pass
        row[-1] = timestamp_value  # XXX: this should be append
        fh.append(row)


if __name__ == "__main__":
    main()
