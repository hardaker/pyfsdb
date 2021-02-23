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
                        help="The two columns to use for the x and y axes")

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

    parser.add_argument("--label-column", default=None, type=str,
                        help="Column to use for labeling the squares")

    parser.add_argument("-fs", "--font-size", default=None, type=int,
                        help="Set the fontsize for labels")

    parser.add_argument("-C", "--cmap", default="Blues_r", type=str,
                        help="matplotlib colormap to use (good choices: Blues_r, gray, PuBu_r, summer_r, YlGn_r)")

    parser.add_argument("--list-cmaps", action="store_true",
                        help="List the colormap values available for -C")

    parser.add_argument("--label-limit", default=30, type=int,
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

    if args.list_cmaps:
        all = plt.colormaps()
        print("\n".join(all))
        exit()

    if not args.columns or len(args.columns) != 2:
        raise ValueError("exactly 2 columns must be passed to -c")

    return args


def maybe_shrink_label(label, length_limit=30):
    label = str(label)
    if len(label) <= length_limit:
        return label
    part_length = int((length_limit-3) / 2) # save room for middle dots
    right_len = -part_length
    return label[0:part_length+1] + "..." + label[right_len:]


def normalize(input_data, columns, value_column, label_column=None):
    """Loops over all of the rows of dict data extracting a tuple of:

     data: the data in array/dict format, normalized to MIN->1.0
     dataset: the dataset in a deep dictonary format
     min_value: the minimum value seen
     max_value: the maximum value seen
     xcols: the list of x column labels
     ycols: the list of y column labels
     labelset: the labels in a deep dictonary format if label_column was specified"""
    # loop over all the rows calculating the min/max values and save results
    min_value = None
    max_value = None
    ycols = {}  # stores each unique second value
    dataset = {}  # nested tree structure
    labelset = {}

    for row in input_data:
        if not max_value:
            max_value = float(row[value_column])
        else:
            max_value = max(max_value, float(row[value_column]))

        if not min_value:
            min_value = float(row[value_column])
        else:
            min_value = min(min_value, float(row[value_column]))

        label = None
        x_value = row[columns[0]]
        y_value = row[columns[1]]
        value = row[value_column]
        if label_column and label_column in row:
            label = row[label_column]
        if x_value not in dataset:
            dataset[x_value] = {y_value: float(value)}
        else:
            dataset[x_value][y_value] = float(value)

        # set the optional labels
        if label:
            if x_value not in labelset:
                labelset[x_value] = {y_value: label}
            else:
                labelset[x_value][y_value] = label

        ycols[y_value] = 1

    # merge the data into a two dimensional array
    data = []
    xcols = sorted(dataset.keys())
    ycols = sorted(ycols.keys())
    for first_column in xcols:
        newrow = []
        for second_column in ycols:
            if second_column in dataset[first_column] and max_value > 0:
                val = dataset[first_column][second_column] / max_value
                newrow.append(val)
            else:
                newrow.append(0.0)
        data.append(newrow)

    return {'data': data,
            'dataset': dataset,
            'min_value': min_value,
            'max_value': max_value,
            'xcols': xcols,
            'ycols': ycols,
            'labelset': labelset}


def create_heat_map(input_data, columns, value_column,
                    add_labels=False, add_raw=False,
                    add_fractions=False, invert=False,
                    font_size=None, max_label_size=20,
                    cmap='Blues_r', label_column=None):

    results = normalize(input_data, columns, value_column, label_column)

    (data, dataset, xcols, ycols, labelset) = \
        (results['data'],
         results['dataset'],
         results['xcols'],
         results['ycols'],
         results['labelset'])

    grapharray = np.array(data)
    if not invert:
        grapharray = 1 - grapharray

    # generate the graph
    fig, ax = plt.subplots()

    # set the size
    fig.set_dpi(150)
    fig.set_size_inches(16, 9)

    ax.imshow(grapharray, vmin=0.0, vmax=1.0, cmap=cmap)
    # ax.grid(ls=':')

    ax.set_xlabel(maybe_shrink_label(columns[1], max_label_size), fontsize=font_size)
    ax.set_ylabel(maybe_shrink_label(columns[0], max_label_size), fontsize=font_size)

    # note: xlabels are applied on the y tick labels
    if add_labels:
        ax.set_yticks(np.arange(len(dataset)))
        ax.set_xticks(np.arange(len(ycols)))

        xlabels = [maybe_shrink_label(x, max_label_size) for x in xcols]
        ax.set_yticklabels(xlabels, fontsize=font_size)

        ylabels = [maybe_shrink_label(y, max_label_size) for y in ycols]
        ax.set_xticklabels(ylabels, fontsize=font_size)

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
                        ax.text(j, i, "{:1.1f}".format(float(value)),
                                ha="center", va="center", color="r",
                                fontsize=font_size)
                except Exception:
                    pass

    elif label_column:
        for i, first_column in enumerate(xcols):
            for j, second_column in enumerate(ycols):
                try:
                    label = labelset[first_column][second_column]
                    if label:
                        ax.text(j, i, str(label),
                                ha="center", va="center", color="r",
                                fontsize=font_size)
                except Exception:
                    pass

    fig.tight_layout()
    return (fig, data, dataset)


def main():
    args = parse_args()

    # read in the input data
    f = pyfsdb.Fsdb(file_handle=args.input_file,
                    return_type=pyfsdb.RETURN_AS_DICTIONARY)

    (fig, data, dataset) = \
        create_heat_map(f, args.columns, args.value_column,
                        args.add_labels, args.add_raw,
                        args.add_fractions, args.invert,
                        args.font_size, args.label_limit,
                        args.cmap, args.label_column)

    fig.savefig(args.output_file,
                bbox_inches="tight", pad_inches=0)

    # import pprint
    # pprint.pprint(dataset)


if __name__ == "__main__":
    main()
