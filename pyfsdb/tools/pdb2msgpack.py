#!/usr/bin/python

"""Converts a textual FSDB representation to a efficient msgpack binary encoding"""

import pyfsdb

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys

# optionally use rich
try:
    from rich import print
    from rich.logging import RichHandler
except Exception:
    pass


def parse_args():
    "Parse the command line arguments."
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: ",
    )

    parser.add_argument("-y", "--full-arg", default="full-arg", type=str, help="help")

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "input_file", type=FileType("r"), nargs="?", default=sys.stdin, help=""
    )

    parser.add_argument(
        "output_file", type=FileType("wb"), nargs="?", default=sys.stdout, help=""
    )

    args = parser.parse_args()
    log_level = args.log_level.upper()
    handlers = []
    datefmt = None
    messagefmt = "%(levelname)-10s:\t%(message)s"

    # see if we're rich
    try:
        handlers.append(RichHandler(rich_tracebacks=True))
        datefmt = " "
        messagefmt = "%(message)s"
    except Exception:
        pass

    logging.basicConfig(
        level=log_level, format=messagefmt, datefmt=datefmt, handlers=handlers
    )
    return args


def main():
    args = parse_args()

    in_fsdb = pyfsdb.Fsdb(
        file_handle=args.input_file,
        return_type=pyfsdb.RETURN_AS_ARRAY,
    )

    # eventually:
    import io

    outfile = io.StringIO()
    out_fsdb = pyfsdb.Fsdb(
        # out_file_handle=args.output_file,
        out_file_handle=outfile,
        out_column_names=in_fsdb.column_names,
    )
    out_fsdb.out_separator_token = "m"  # save as msgpack

    oh = args.output_file
    oh.write(bytes(out_fsdb.out_header_line, encoding="utf-8"))

    # for now
    import msgpack

    # for record in in_fsdb:
    for row in in_fsdb:
        oh.write(msgpack.packb(row, use_bin_type=True))


if __name__ == "__main__":
    main()
