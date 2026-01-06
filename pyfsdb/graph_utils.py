from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, Namespace


def parse_args(
    parser: ArgumentParser, sub_group_name: str = "Graph options"
) -> Namespace:
    """Adds graphing specific arguments to the current parser.

    Puts contents in a sub-group unless sub_group_name is None."""

    parser.add_argument(
        "-x", "--x-column", default=["x"], type=str, help="X-axis column name to use"
    )

    parser.add_argument(
        "--xs",
        "--x-is-seconds",
        action="store_true",
        help="The X axis is epoch seconds since Jan 1, 1970",
    )

    parser.add_argument(
        "--xd",
        "--x-is-datestamp",
        action="store_true",
        help="The X axis is a date stamp (eg: 2025-01-01)",
    )

    parser.add_argument(
        "-y",
        "--y-column",
        default="value",
        type=str,
        help="Y-axis column name to use",
    )

    parser.add_argument(
        "-Y",
        "--style-column",
        default=None,
        type=str,
        help="Variable to use for changing marker styles",
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


def set_graph_paremeters(plt, fig, args: Namespace):
    """Set titles, labels, etc according to arguments passed."""

    if args.title:
        fig.set(title=args.title)
    if args.xlabel:
        fig.set_xlabels(args.xlabel)
    if args.ylabel:
        fig.set_ylabels(args.ylabel)
    print("here")


def output_plot(plt, output_file, args):
    """Actually save the file and set some other plot defaults."""

    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
