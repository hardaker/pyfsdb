from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace
from matplotlib.axes import Axes
from seaborn.axisgrid import FacetGrid


def parse_args(
    parser: ArgumentParser, sub_group_name: str = "Graph options"
) -> ArgumentParser:
    """Adds graphing specific arguments to the current parser.

    Puts contents in a sub-group unless sub_group_name is None."""

    if sub_group_name:
        parser = parser.add_argument_group(sub_group_name)

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
        "--yr",
        "--y-label-rotation",
        "--",
        default=45,
        type=int,
        help="Amount to rotate the Y labels by.",
    )

    parser.add_argument(
        "-t", "--title", default=None, type=str, help="Title to place to the top"
    )

    parser.add_argument(
        "--xlabel", default=None, type=str, help="Text to use for the X axis label"
    )

    parser.add_argument(
        "--ylabel", default=None, type=str, help="Text to use for the Y axis label"
    )

    parser.add_argument(
        "--dpi", default=200, type=int, help="The DPI to use in the resulting image"
    )

    return parser


def set_graph_parameters(control: Axes | FacetGrid, args: Namespace):
    """Set titles, labels, etc according to arguments passed."""

    if args.title:
        control.set(title=args.title)
    if args.xlabel:
        control.set(xlabel=args.xlabel)
    if args.ylabel:
        control.set(ylabel=args.ylabel)


def output_plot(plt, output_file, args):
    """Actually save the file and set some other plot defaults."""

    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.xticks(rotation=args.yr)
    plt.tight_layout()
    plt.savefig(output_file, dpi=args.dpi)
