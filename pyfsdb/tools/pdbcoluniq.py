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

    parser.add_argument("-k", "--keys", default=["key"], type=str, nargs="*",
                        help="Key to use when counting for uniqueness")

    parser.add_argument("-c", "--count", action="store_true",
                        help="Count the columns")

    parser.add_argument("-i", "--initial-count-column", default=None, type=str,
                        help="The input data already has this count column to aggregate together")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="")

    args = parser.parse_args()
    return args


def output_results(outh, keys, data, count=False):
    for subkey in data:
        if isinstance(data[subkey], dict):
            output_results(outh, keys + [subkey], data[subkey], count)
        else:
            if count:
                outh.append(keys + [subkey, data[subkey]])
            else:
                outh.append(keys + [subkey])


def filter_unique_columns(in_file_handle, out_file_handle, keys,
                          count=False, initial_count_key=None):
    fh = pyfsdb.Fsdb(file_handle=in_file_handle)
    ofh = pyfsdb.Fsdb(out_file_handle=out_file_handle)

    key_columns = fh.get_column_numbers(keys)
    initial_count_col = None
    if initial_count_key:
        initial_count_col = fh.get_column_number(initial_count_key)

    if initial_count_col:
        count = True

    # set the output column names
    if count:
        ofh.column_names = keys + ['count']
    else:
        ofh.column_names = keys

    num_keys = len(keys)
    if len(key_columns) == 1:
        counters = collections.Counter()
        for row in fh:
            if initial_count_col:
                counters[row[key_columns[0]]] += int(row[initial_count_col])
            else:
                counters[row[key_columns[0]]] += 1
    else:
        counters = {}
        for row in fh:
            pointer = counters
            for keynum in range(num_keys - 2):
                this_value = row[key_columns[keynum]]
                if this_value not in pointer:
                    pointer[this_value] = {}
                pointer = pointer[this_value]

            this_value = row[key_columns[num_keys - 2]]
            final_value = row[key_columns[-1]]
            if this_value not in pointer:
                pointer[this_value] = collections.Counter()
            if initial_count_col:
                pointer[this_value][final_value] += int(row[initial_count_col])
            else:
                pointer[this_value][final_value] += 1


    # output the results, with optional counts
    # (if statement at outer tier for speed)
    output_results(ofh, [], counters, count)

    ofh.close()


def main():
    args = parse_args()

    filter_unique_columns(args.input_file, args.output_file,
                          keys=args.keys, count=args.count,
                          initial_count_key=args.initial_count_column)


if __name__ == "__main__":
    main()
