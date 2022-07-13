#!/usr/bin/python3

"""Load a parquet file and convert it to FSDB, with an optional column
and filter list"""

import pyfsdb

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: parque2fsdb -c col1 col2 -- file.parquet file.fsdb")

    parser.add_argument("-c", "--columns", nargs="*",
                        type=str, help="Columns to load")

    parser.add_argument("-f", "--filters", nargs="*",
                        type=str, help="Filters to apply to the data [format tbd]")

    parser.add_argument("-l", "--line-by-line", action="store_true",
                        help="Read the parquet file line by line instead of all at once (slower)")

    parser.add_argument("input_file", type=str,
                        help="The input parquet file to load")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output FSDB file")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    try:
        import fastparquet
    except Exception:
        error("Failed to load the fastparquet python module: use 'pip install fastparquet' to install it.")
        exit()

    fh = pyfsdb.Fsdb(out_file_handle=args.output_file)
    pf = fastparquet.ParquetFile(args.input_file)

    if args.line_by_line:
        for df in pf.iter_row_groups(columns=args.columns):
            fh.put_pandas(df)
    else:
        df = pf.to_pandas(columns=args.columns)
        fh.put_pandas(df)


if __name__ == "__main__":
    main()
