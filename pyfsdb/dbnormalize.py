#!/usr/bin/python3

"""dbnormalize takes an input file and takes each column value from a
number of columns and divides it by the maximum value seen in all the
columns.

Note: this is the maximum value of all columns provided; if you want
per-column normalization, run the tool multiple times instead.

Note: this requires reading the entire file into memory.
"""

import pyfsdb
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: dbnormalize -k column -- infile outfile")

    parser.add_argument("-k", "--keys", default=["key"], nargs="+", type=str,
                        help="The columns/keys to normalize across")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file to read")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Where to write the results")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    fh = pyfsdb.Fsdb(file_handle=args.input_file,
                     out_file_handle=args.output_file)
    df = fh.get_pandas()
    maxval = df[args.keys].max().max()
    for key in args.keys:
        df[key] = df[key] / maxval
    fh.put_pandas(df)
    fh.close()


if __name__ == "__main__":
    main()
