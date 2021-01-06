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

    if (not args. values or len(args.values) == 0) \
       and not args.include_all_values:
            sys.stderr.write("Either -v or -V is required\n")
            exit(1)

    return args

def dump_remaining(fsh, struct, empty_num, key_cols, value_cols):
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

            # append the created row
            fsh.append(row)
        return
    else:
        # we're not fully deep in the tree, keep diving
        for item in struct:
            dump_remaining(fsh, struct[item], empty_num,
                           key_cols, value_cols)

def main():
    args = parse_args()

    # read in the augument file entirely first
    augh = pyfsdb.Fsdb(file_handle = args.augment_file,
                       return_type=pyfsdb.RETURN_AS_DICTIONARY)

    # store each row based on its list of keys, but storing
    # each additional key as a deeper layer of dictionaries.
    # the final key used is 'data' to store the data itself
    savestruct = {}
    for row in augh:
        current = savestruct
        # traverse/create the nested structure
        for key in args.keys:
            if row[key] not in current:
                current[row[key]] = {}
            current = current[row[key]]
        current['data'] = row

    # read in stream file, and augment each row with the new columns
    streamh = pyfsdb.Fsdb(file_handle = args.stream_file)

    # determine which columns need to be added on (potentially all)
    if not args.values or len(args.values) == 0:
        columns = augh.column_names
        args.values = []
        for column in columns:
            if column not in args.keys:
                args.values.append(column)

    # create the output stream to store the data
    outh = pyfsdb.Fsdb(out_file_handle = args.output_file)
    outh.out_column_names = streamh.column_names + args.values

    key_columns = streamh.get_column_numbers(args.keys)

    for row in streamh:
        current = savestruct
        # traverse/create the nested structure
        for key in key_columns:
            if row[key] not in current:
                current = None
                break
            current = current[row[key]]
    
        # on a deep match finding
        if current:
            current['used'] = 1
            current = current['data']
            for value in args.values:
                row.append(current[value])

        outh.append(row)

    # Now loop through all data adding any rows 
    if args.include_unmatched_augment_rows:
        dump_remaining(outh, savestruct,
                       # total original column numbers - key count
                       len(streamh.column_names) - len(args.keys),
                       args.keys, args.values)

if __name__ == "__main__":
    main()
