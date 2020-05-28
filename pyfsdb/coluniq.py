#!/usr/bin/python3

import sys, os
import argparse
import collections

import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

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

def main():
    args = parse_args()
    
    fh = pyfsdb.Fsdb(file_handle=args.input_file)
    ofh = pyfsdb.Fsdb(out_file_handle=args.output_file)

    key_column = fh.get_column_number(args.key)

    # set the output column names
    if args.count:
        ofh.column_names = [args.key, 'count']
    else:
        ofh.column_names = [args.key]

    counters = collections.Counter()
    for row in fh:
        counters[row[key_column]] += 1

    output_keys = counters.keys()
    if args.sort:
        output_keys = sorted(output_keys, reverse=args.reverse_sort)
    elif args.sort_by_count:
        output_keys = sorted(output_keys, key=lambda x: counters[x],
                             reverse=args.reverse_sort)

    # output the results, with optional counts
    # (if statement at outer tier for speed)
    if args.count:
        for output_key in output_keys:
            ofh.append([output_key, counters[output_key]])
    else:
        for output_key in output_keys:
            ofh.append([output_key])

    ofh.write_finish()

if __name__ == "__main__":
    main()

