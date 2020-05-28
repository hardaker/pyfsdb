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

    parser.add_argument("-v", "--values", type=str, nargs="+",
                        help="Value columns to insert on a match")

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
    return args

def main():
    args = parse_args()

    # read in the augument file entirely first
    augh = pyfsdb.Fsdb(file_handle = args.augment_file,
                     return_type=pyfsdb.RETURN_AS_DICTIONARY)
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
    
        if current:
            current = current['data']
            for value in args.values:
                row.append(current[value])

        outh.append(row)

if __name__ == "__main__":
    main()
