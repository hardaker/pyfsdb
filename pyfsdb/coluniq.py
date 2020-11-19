#!/usr/bin/python3

import sys
import os
import argparse
import collections

import pyfsdb


def parse_args():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class,
                                     description=__doc__)

    parser.add_argument("-k", "--key", default="key", type=str,
                        help="Key to use when counting for uniqueness")

    parser.add_argument("-c", "--count", action="store_true",
                        help="Count the columns")

    parser.add_argument("-s", "--sort", action="store_true",
                        help="Sort the results")

    parser.add_argument("-S", "--sort-by-count", action="store_true",
                        help="Sort the results but by count")

    parser.add_argument("-r", "--reverse-sort", action="store_true",
                        help="Sort in reverse order")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="")

    args = parser.parse_args()
    return args


def filter_unique_columns(in_file_handle, out_file_handle, key,
                          count=False, sort=False,
                          reverse_sort=False, sort_by_count=False):
    fh = pyfsdb.Fsdb(file_handle=in_file_handle)
    ofh = pyfsdb.Fsdb(out_file_handle=out_file_handle)

    key_column = fh.get_column_number(key)

    # set the output column names
    if count:
        ofh.column_names = [key, 'count']
    else:
        ofh.column_names = [key]

    counters = collections.Counter()
    for row in fh:
        counters[row[key_column]] += 1

    output_keys = counters.keys()
    if sort:
        output_keys = sorted(output_keys, reverse=reverse_sort)
    elif sort_by_count:
        output_keys = sorted(output_keys, key=lambda x: counters[x],
                             reverse=reverse_sort)

    # output the results, with optional counts
    # (if statement at outer tier for speed)
    if count:
        for output_key in output_keys:
            ofh.append([output_key, counters[output_key]])
    else:
        for output_key in output_keys:
            ofh.append([output_key])

    ofh.close()


def main():
    args = parse_args()

    filter_unique_columns(args.input_file, args.output_file,
                          count=args.count, sort=args.sort,
                          reverse_sort=args.reverse_sort,
                          sort_by_count=args.sort_by_count)


if __name__ == "__main__":
    main()
