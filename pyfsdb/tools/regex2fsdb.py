"""Create an FSDB file from anything else using regular expressions."""

from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace
from logging import debug, info, warning, error, critical
import logging
import sys
import re
import pyfsdb

# optionally use rich
try:
    from rich import print
    from rich.logging import RichHandler
    from rich.theme import Theme
    from rich.console import Console
except Exception:
    debug("install rich and rich.logging for prettier results")

# optionally use rich_argparse too
help_handler = ArgumentDefaultsHelpFormatter
try:
    from rich_argparse import RichHelpFormatter

    help_handler = RichHelpFormatter
except Exception:
    debug("install rich_argparse for prettier help")


def parse_args() -> Namespace:
    """Parse the command line arguments."""
    parser = ArgumentParser(
        formatter_class=help_handler, description=__doc__, epilog="Example Usage: "
    )

    parser.add_argument(
        "-c",
        "--columns",
        default=None,
        type=str,
        nargs="*",
        help="A list of column names to use in the output (one per match group)",
    )

    parser.add_argument(
        "-r",
        "--regex",
        type=str,
        help="The regular expression to use when processing the file.",
    )

    parser.add_argument(
        "-i",
        "--ignore-case",
        action="store_true",
        help="Ignore case when finding matches.",
    )

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
        "output_file", type=FileType("w"), nargs="?", default=sys.stdout, help=""
    )

    args = parser.parse_args()
    log_level = args.log_level.upper()
    handlers = []
    datefmt = None
    messagefmt = "%(levelname)-10s:\t%(message)s"

    # see if we're rich
    try:
        handlers.append(
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                console=Console(
                    stderr=True, theme=Theme({"logging.level.success": "green"})
                ),
            )
        )
        datefmt = " "
        messagefmt = "%(message)s"
    except Exception:
        debug("failed to install RichHandler")

    logging.basicConfig(
        level=log_level, format=messagefmt, datefmt=datefmt, handlers=handlers
    )

    if not args.regex:
        error("The --regex (-r) flag is required.")
        exit(1)

    return args


def main():
    args = parse_args()

    columns = args.columns
    searcher = re.compile(args.regex)

    flags = 0
    if args.ignore_case:
        flags |= re.IGNORECASE

    with pyfsdb.Fsdb(
        out_file_handle=args.output_file, out_column_names=columns
    ) as outh:
        for line in args.input_file:
            line = line.strip()
            match = searcher.match(line)
            if match:
                data = match.groups()

                if len(data) != len(args.columns):
                    error(
                        "warning, matching did not produce the right number of columns"
                    )
                    error(f"  line:   {line}")
                    error(f"  cols:   {columns}")
                    error(f"  groups: {data}")

                else:
                    outh.append(data)


if __name__ == "__main__":
    main()
