#!/usr/bin/python3

"""Save an FSDB file to an apache parquet file"""

import pyfsdb
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys
import logging

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: fsdb2parquet -c col1 col2 -- file.fsdb file.parquet ")

    parser.add_argument("-c", "--categories", nargs="*",
                        type=str, help="Columns to declare as categories")

    parser.add_argument("-C", "--compression-type", default="GZIP", type=str,
                        help="The compression type to use (SNAPPY or GZIP)")

    parser.add_argument("-l", "--compression-level", default=None, type=int,
                        help="The compression level to pass to the algorithm")

    parser.add_argument("-o", "--row-offsets", default=50000000, type=int,
                        help="Row size to write")

    parser.add_argument("-f", "--fast-read", action="store_true",
                        help="If the dataset does not contain # characters, this can be used")

    parser.add_argument("input_file", type=FileType('r'),
                        help="The input fsdb file to load (can be - for stdin)")

    parser.add_argument("output_file", type=str,
                        help="The output parquet file to write")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    try:
        import pyarrow.parquet
    except Exception:
        error("Failed to load the pyarrow python module: use 'pip install pyarrow' to install it.")
        exit()

    fh = pyfsdb.Fsdb(file_handle=args.input_file)

    df = fh.get_pandas(data_has_comment_chars=(not args.fast_read))

    if args.categories:
        for column in args.categories:
            df[column] = df[column].astype('category')

    table = pyarrow.Table.from_pandas(df)
    pyarrow.parquet.write_table(table, args.output_file,
                                compression=args.compression_type,
                                compression_level=args.compression_level)


if __name__ == "__main__":
    main()
