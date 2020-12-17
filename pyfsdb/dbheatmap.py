#!/usr/bin/python3

import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pyfsdb


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: ")

    parser.add_argument("-c", "--columns", type=str, nargs=2,
                        help="Columns to use")

    parser.add_argument("-v", "--value-column", default="count", type=str,
                        help="The value column to plot as the heat map")

    parser.add_argument("-i", "--invert", action="store_true",
                        help="Invert the foreground/background colors")

    parser.add_argument("-F", "--add-fractions", action="store_true",
                        help="Add text fraction labels to the grid")

    parser.add_argument("-R", "--add-raw", action="store_true",
                        help="Add text raw-value labels to the grid")

    parser.add_argument("-L", "--add-labels", action="store_true",
                        help="Add x/y axis labels")

    parser.add_argument("-fs", "--font-size", default=None, type=int,
                        help="Set the fontsize for labels")

    parser.add_argument("--label-limit", default=40, type=int,
                        help="The maximum length of a label;" +
                        "  If longer, truncate with ...s in the middle. " +
                        "Use 0 if infinite is desired.")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="Input fsdb file to read")

    parser.add_argument("output_file", type=str,
                        nargs='?', default="out.png",
                        help="Where to write the png file to")

    args = parser.parse_args()

    if not args.columns or len(args.columns) != 2:
        raise ValueError("exactly 2 columns must be passed to -c")

    return args


def maybe_shrink_label(label, length_limit=40):
    if len(label) <= length_limit:
        return label
    return label[0:length_limit-1] + "..." + label[- length_limit-2:]


def create_heat_map(input_data, columns, value_column,
                    add_labels=False, add_raw=False,
                    add_fractions=False, invert=False,
                    font_size=None, max_label_size=20):
    max_value = None
    dataset = {}  # nested tree structure
    ycols = {}  # stores each unique second value
    for row in input_data:
        if not max_value:
            max_value = float(row[value_column])
        else:
            max_value = max(max_value, float(row[value_column]))

        if row[columns[0]] not in dataset:
            dataset[row[columns[0]]] = \
                {row[columns[1]]: float(row[value_column])}
        else:
            dataset[row[columns[0]]][row[columns[1]]] = \
                float(row[value_column])
        ycols[row[columns[1]]] = 1

    # merge the data into a two dimensional array
    data = []
    xcols = sorted(dataset.keys())
    ycols = sorted(ycols.keys())
    for first_column in xcols:
        newrow = []
        for second_column in ycols:
            if second_column in dataset[first_column]:
                newrow.append(dataset[first_column][second_column] / max_value)
            else:
                newrow.append(0.0)
        data.append(newrow)

    grapharray = np.array(data)
    if not invert:
        grapharray = 1 - grapharray

    # generate the graph
    fig, ax = plt.subplots()

    # set the size
    fig.set_dpi(150)
    fig.set_size_inches(16,9)

    ax.imshow(grapharray, vmin=0.0, vmax=1.0, cmap='Pastel1')
    # ax.grid(ls=':')

    ax.set_xlabel(maybe_shrink_label(columns[1], max_label_size))
    ax.set_ylabel(maybe_shrink_label(columns[0], max_label_size))

    # note: xlabels are applied on the y tick labels
    if add_labels:
        ax.set_yticks(np.arange(len(dataset)))
        ax.set_xticks(np.arange(len(ycols)))

        xlabels = [maybe_shrink_label(x, max_label_size) for x in xcols]
        ax.set_yticklabels(xlabels)

        ylabels = [maybe_shrink_label(y, max_label_size) for y in ycols]
        ax.set_xticklabels(ylabels)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

    if add_fractions:
        for i in range(len(grapharray)):
            for j in range(len(grapharray[i])):
                ax.text(j, i, "{:1.1f}".format(grapharray[i][j]),
                        ha="center", va="center", color="r",
                        fontsize=font_size)
    elif add_raw:
        for i, first_column in enumerate(xcols):
            for j, second_column in enumerate(ycols):
                try:
                    value = dataset[first_column][second_column]
                    if value != "0" and value != 0:
                        ax.text(j, i, "{}".format(int(value)),
                                ha="center", va="center", color="r",
                                fontsize=font_size)
                except Exception:
                    pass

    fig.tight_layout()
    return fig


def main():
    args = parse_args()

    # read in the input data
    f = pyfsdb.Fsdb(file_handle=args.input_file,
                    return_type=pyfsdb.RETURN_AS_DICTIONARY)

    fig = create_heat_map(f, args.columns, args.value_column,
                          args.add_labels, args.add_raw,
                          args.add_fractions, args.invert,
                          args.font_size, args.label_limit)

    fig.savefig(args.output_file,
                bbox_inches="tight", pad_inches=0)

    # import pprint
    # pprint.pprint(dataset)


if __name__ == "__main__":
    main()
