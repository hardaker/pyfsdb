"""Create a SANKEY diagram from FSDB data."""

from __future__ import annotations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace
from logging import debug, info, warning, error, critical
import logging
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame
import pyfsdb

try:
    import plotly.graph_objects
    import kaleido
except Exception:
    error("The plotly and kaleido python modules are required for pdbsankey to work.")
    sys.exit(1)

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
        "-s",
        "--source-column",
        default="source",
        type=str,
        help="The column to use as the source.",
    )

    parser.add_argument(
        "-d",
        "--destination-column",
        default="destination",
        type=str,
        help="The column to use as the destination.",
    )

    parser.add_argument(
        "-c",
        "--count-column",
        default="count",
        type=str,
        help="The column to use as the count from source to destination.",
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
        "output_file",
        type=FileType("wb"),
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

    columns = [args.source_column, args.destination_column, args.count_column]
    counts = []

    sources = []
    destinations = []
    counts = []

    column_name_map = {}
    column_count = 0

    with pyfsdb.Fsdb(file_handle=args.input_file) as inh:
        column_nums = inh.get_column_numbers(columns)
        for row in inh:
            source = row[column_nums[0]]
            destination = row[column_nums[1]]

            if source not in column_name_map:
                column_name_map[source] = column_count
                column_count += 1

            if destination not in column_name_map:
                column_name_map[destination] = column_count
                column_count += 1

            sources.append(column_name_map[source])
            destinations.append(column_name_map[destination])
            counts.append(row[column_nums[2]])

    sankey = plotly.graph_objects.Sankey(
        node={
            "pad": 15,
            "thickness": 20,
            "line": {"color": "black", "width": 0.5},
            "label": list(column_name_map.keys()),
            "color": "blue",
        },
        link={
            "source": sources,
            "target": destinations,
            "value": counts,
        },
    )

    fig = plotly.graph_objects.Figure(data=[sankey])
    fig.update_layout(title_text="", font_size=10)

    args.output_file.write(fig.to_image("png"))


if __name__ == "__main__":
    main()
