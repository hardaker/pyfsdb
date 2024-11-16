"""Converts a msgpack FSDB representation to a normal FSDB text file"""

import pyfsdb

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import io

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

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "input_file", type=FileType("rb"), nargs="?", default=sys.stdin, help=""
    )

    parser.add_argument(
        "output_file", type=FileType("w"), nargs="?", default=sys.stdout, help=""
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

    oh = pyfsdb.Fsdb(
        out_file_handle=args.output_file,
        out_column_names=in_fsdb.column_names,
    )

    for row in in_fsdb:
        oh.append(row)


if __name__ == "__main__":
    main()
