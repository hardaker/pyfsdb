#!/usr/bin/python3

"""This script expects to augment a FSDB stream (or file) with
   additional information found in another FSDB file.  The second file
   is loaded entirely into memory in order to accomplish this.  Any
   row in the stream file that has exactly matching keys in the second
   file will be augmented to using data from the 'values' columns is
   the augment file.

   This duplicates dbjoin to a large extent, but dbaugment is faster
   when one side is small because it avoids sorting.  dbaugment can
   also operate on streaming data, since sorting isn't required.
"""

import argparse
import sys
import os

import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("-k", "--keys", default=['timestamp', 'key'], type=str, nargs="+",
                        help="Keys to match against")

    parser.add_argument("-v", "--values", type=str, nargs="*",
                        help="Value columns to insert on a match")

    parser.add_argument("-V", "--include-all-values", action="store_true",
                        help="Include all the value columns from the matching row")

    parser.add_argument("-i", "--include-unmatched-augment-rows", action="store_true",
                        help="Include (at the bottom) any rows from the augment file that failed to match any stream rows.")

    parser.add_argument("-n", "--mark-new", type=str,
                        help="Mark new columns in `stream_file` not present in `augument_file` with a 1 in this new column name, else a 0")

    parser.add_argument("stream_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("augment_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="")

    args = parser.parse_args()

    if ((not args. values or len(args.values) == 0) and not args.mark_new) \
       and not args.include_all_values:
            sys.stderr.write("Either -v, -V or -n is required\n")
            exit(1)

    return args


def dump_remaining(fsh, struct, empty_num, key_cols, value_cols, mark_new=None):
    """Adds remaining unseen records in the stored augment file into the
    output handle.  Recursion used to descend a deep-encoded
    structure.
    """
    if 'data' in struct:
        # end condition
        if 'used' not in struct:
            # unused row found,
            # construct the output row, consisting of keys
            # followed by blanks, followed by values
            # XXX: this breaks when the keys aren't the first columns
            row = []
            for key in key_cols:
                row.append(struct['data'][key])
            row.extend([''] * empty_num)
            for value in value_cols:
                row.append(struct['data'][value])
            if mark_new:
                row.append(1)

            # append the created row
            fsh.append(row)
        return
    else:
        # we're not fully deep in the tree, keep diving
        for item in struct:
            dump_remaining(fsh, struct[item], empty_num,
                           key_cols, value_cols, mark_new=mark_new)


def stash_row(cache, key_list, row):
    """Stashes a row in a depth tree based on the keys in the row, the
    cache should be initialized to an empty dictonary on the first
    call."""
    # store each row based on its list of keys, but storing
    # each additional key as a deeper layer of dictionaries.
    # the final key used is 'data' to store the data itself

    # traverse/create the nested structure
    current = cache
    for key in key_list:
        if row[key] not in current:
            current[row[key]] = {}
        current = current[row[key]]
    current['data'] = row


def find_row(cache, key_list, row, return_data=True):
    """Finds a row in a stash given a list of keys matching a passed in
       row.  Any matches will be marked as used too.  If `return_data`
       is true, the cached data itself will be returned, otherwise the
       cache pointer above it will be returned with 'data' as a
       sub-key to the cache point.

    """
    # traverse/create the nested structure
    current = cache
    for key in key_list:
        if row[key] not in current:
            current = None
            break
        current = current[row[key]]

    if return_data:
        return current['data'];
    return current


def main():
    args = parse_args()

    # read in the augument file entirely first
    augh = pyfsdb.Fsdb(file_handle = args.augment_file,
                       return_type=pyfsdb.RETURN_AS_DICTIONARY)

    # store each row based on its list of keys, but storing
    # each additional key as a deeper layer of dictionaries.
    # the final key used is 'data' to store the data itself
    cache = {}
    for row in augh:
        stash_row(cache, args.keys, row)

    # read in stream file, and augment each row with the new columns
    streamh = pyfsdb.Fsdb(file_handle = args.stream_file)

    # determine which columns need to be added on (potentially all)
    if args.include_all_values or \
       ((not args.values or len(args.values) == 0) and not args.mark_new):
        columns = augh.column_names
        args.values = []
        for column in columns:
            if column not in args.keys:
                args.values.append(column)
    elif not args.values:
        args.values = []

    # create the output stream to store the data
    outh = pyfsdb.Fsdb(out_file_handle=args.output_file)
    other_columns = []
    if args.mark_new:
        other_columns = [args.mark_new]
    outh.out_column_names = streamh.column_names + args.values + other_columns

    key_columns = streamh.get_column_numbers(args.keys)

    for row in streamh:
        # traverse/create the nested structure
        current = find_row(cache, key_columns, row, return_data=False)

        # on a deep match finding
        if current:
            current['used'] = 1
            current = current['data']
            for value in args.values:
                row.append(current[value])
            if args.mark_new:
                row.append(0)
        elif args.mark_new:
            row.extend([None] * len(args.values) + [1])

        outh.append(row)

    # Now loop through all data adding any rows
    if args.include_unmatched_augment_rows:
        dump_remaining(outh, cache,
                       # total original column numbers - key count
                       len(streamh.column_names) - len(args.keys),
                       args.keys, args.values,
                       mark_new=args.mark_new)


if __name__ == "__main__":
    main()
