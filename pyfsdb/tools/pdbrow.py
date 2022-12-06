"""Selects rows based on python boolean expressions"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import pyfsdb


def parse_args():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: ",
    )

    parser.add_argument(
        "-c",
        "--data-column",
        default="data",
        type=str,
        help="The input column name to create a CDF from",
    )

    parser.add_argument(
        "-C",
        "--cdf-column",
        default=None,
        type=str,
        help="The output CDF column name -- if none, '_cdf' will be appended to --column",
    )

    parser.add_argument(
        "-R",
        "--raw-column",
        default=None,
        type=str,
        help="Output raw accumulating count to this column",
    )

    parser.add_argument(
        "-P",
        "--percent-column",
        default=None,
        type=str,
        help="Output a percentage column, in addition to the CDF column",
    )

    parser.add_argument(
        "-F",
        "--fraction-column",
        default=None,
        type=str,
        help="Output a percentage column, in addition to the CDF column",
    )

    parser.add_argument(
        "--log-level", default="info", help="Define the logging verbosity level."
    )

    parser.add_argument(
        "input_file",
        type=FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="The input FSDB file",
    )

    parser.add_argument(
        "output_file",
        type=FileType("w"),
        nargs="?",
        default=sys.stdout,
        help="Where to write the output FSDB to",
    )

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")
    return args


def process_pdbrow(
        input_file,
        output_file,
        expression,
):
    # open input and output fsdb handles
    fh = pyfsdb.Fsdb(file_handle=input_file, return_type=pyfsdb.RETURN_AS_DICTIONARY)
    oh = pyfsdb.Fsdb(out_file_handle=output_file)

    # crate output columns
    oh.out_column_names = fh.column_names

    # process the rows
    for row in fh:
        oh.append(row)


def main():
    args = parse_args()

    process_pdbrow(
        args.input_file,
        args.output_file,
        args.expression,
    )


if __name__ == "__main__":
    main()

