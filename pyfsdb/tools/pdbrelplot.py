"""Plot parts of an FSDB file."""

from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace
from logging import debug, info, warning, error, critical
import logging
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame
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
    debug("install rich_argparse.logging for prettier help")


def parse_args() -> Namespace:
    """Parse the command line arguments."""
    parser = ArgumentParser(
        formatter_class=help_handler, description=__doc__, epilog="Example Usage: "
    )

    parser.add_argument(
        "-x", "--x-column", default=["x"], type=str, help="X-axis column name to use"
    )

    parser.add_argument(
        "-y",
        "--y-column",
        default="value",
        type=str,
        help="Y-axis column name to use",
    )

    parser.add_argument(
        "-H",
        "--hue-column",
        default=None,
        type=str,
        help="Variable to use for changing hue values",
    )

    parser.add_argument(
        "-S",
        "--size-column",
        default=None,
        type=str,
        help="Variable to use for changing marker sizes",
    )

    parser.add_argument(
        "-Y",
        "--style-column",
        default=None,
        type=str,
        help="Variable to use for changing marker styles",
    )

    parser.add_argument(
        "-C",
        "--col-column",
        default=None,
        type=str,
        help="Variable to use for adding multiple columns of plots.",
    )

    parser.add_argument(
        "-R",
        "--row-column",
        default=None,
        type=str,
        help="Variable to use for adding multiple rows of plots.",
    )

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "-s",
        "--scatter-plot",
        action="store_true",
        help="Use a scatter plot instead of a line plot",
    )

    parser.add_argument(
        "input_file", type=FileType("r"), nargs="?", default=sys.stdin, help=""
    )

    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        default="plot.png",
        help="Where to save the output PNG file.",
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
    return args


def main():
    args = parse_args()

    kind: str = "line"
    hue: str | None = None
    style: str | None = None
    size: str | None = None
    col: str | None = None
    row: str | None = None

    sns.set_theme()

    columns = [args.x_column, args.y_column]

    if args.hue_column:
        hue = args.hue_column
        columns.append(args.hue_column)

    if args.size_column:
        size = args.size_column
        columns.append(args.size_column)

    if args.style_column:
        style = args.style_column
        columns.append(args.style_column)

    if args.col_column:
        col = args.col_column
        columns.append(args.col_column)

    if args.row_column:
        row = args.row_column
        columns.append(args.row_column)

    df = pyfsdb.Fsdb(file_handle=args.input_file).get_pandas(usecols=columns)

    if args.scatter_plot:
        kind = "scatter"

    sns.relplot(
        data=df,
        kind=kind,
        x=args.x_column,
        y=args.y_column,
        hue=hue,
        style=style,
        size=size,
        col=col,
        row=row,
        aspect=1.77,
    )

    plt.xticks(rotation=45)
    plt.savefig(args.output_file)


if __name__ == "__main__":
    main()
