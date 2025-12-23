"""Tracks results from IDs as they traverse logical paths.  Useful for sankeys."""

import sys
import os
import argparse
import collections

import pyfsdb
from rich import print


def parse_args():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=formatter_class, description=__doc__
    )

    parser.add_argument(
        "-i",
        "--id-column",
        default="id",
        type=str,
        help="List of ID columns to use for tracking",
    )

    parser.add_argument(
        "-c",
        "--category-column",
        default=None,
        type=str,
        help="The category column to use when tracking IDs that migrate from one category to the next.",
    )

    parser.add_argument(
        "-v",
        "--value-column",
        default="value",
        type=str,
        help="The value column to sue for tracking.",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        type=argparse.FileType("w"),
        nargs="?",
        default=sys.stdout,
        help="Where to save the output tracking results to.",
    )

    parser.add_argument(
        "-C",
        "--append-counts",
        action="store_true",
        help="Add count strings to the end of the names in the image.",
    )

    parser.add_argument(
        "input_files",
        type=argparse.FileType("r"),
        nargs="*",
        default=[sys.stdin],
        help="Input files to use",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    tracking_info = collections.defaultdict(collections.Counter)
    tracking_counts = collections.Counter()
    last_values = collections.defaultdict(str)
    last_categories = collections.defaultdict(str)

    for file_handle in args.input_files:
        with pyfsdb.Fsdb(file_handle=file_handle) as inh:
            (id_col_num, val_col_num) = inh.get_column_numbers(
                [args.id_column, args.value_column]
            )

            cat_col_num = -1
            if args.category_column:
                cat_col_num = inh.get_column_number(args.category_column)
            category_prefix = ""

            for row in inh:
                # get a category prefix
                if cat_col_num > -1:
                    category_prefix = str(row[cat_col_num]) + ":"
                    if not category_prefix:
                        category_prefix = "no_category:"

                this_id = row[id_col_num]

                # if this id was seen before, increase the count between the
                # last value and the current one with a prefix being prepended to both

                # TODO(hardaker): allow for auto-adding/merging of
                # values when id/category pairs are are repeated?
                if this_id in last_values and (
                    category_prefix == "" or last_categories[this_id] != category_prefix
                ):
                    source = last_categories[this_id] + str(last_values[this_id])
                    destination = category_prefix + str(row[val_col_num])
                    tracking_info[source][destination] += 1
                    tracking_counts[source] += 1
                    tracking_counts[destination] += 1

                # save this id's value
                last_values[this_id] = row[val_col_num]
                last_categories[this_id] = category_prefix

    with pyfsdb.Fsdb(out_file_handle=args.output_file) as outh:
        outh.out_column_names = ["source", "destination", "count"]
        for left in tracking_info:
            for right in tracking_info[left]:
                left_name = left
                right_name = right
                if args.append_counts:
                    left_name = (
                        " " + left_name + ": " + str(tracking_counts[left_name]) + " "
                    )
                    right_name = (
                        " " + right_name + ": " + str(tracking_counts[right_name]) + " "
                    )
                outh.append([left_name, right_name, tracking_info[left][right]])


if __name__ == "__main__":
    main()
