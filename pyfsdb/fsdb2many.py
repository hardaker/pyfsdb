#!/usr/bin/python3

"""fsdb2many converts a single FSDB file into many, by creating
other file names based on a column of the original."""

import sys
import argparse
import pyfsdb
import re

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=__doc__,
                                     epilog="fsdb2many -c key -o outputdir/%s.fsdb mybigfile.fsdb")

    parser.add_argument("-c", "--column", default="key", type=str,
                        help="Column to split on")

    parser.add_argument("-o", "--output-pattern",
                        default="fsdb2many-out-%s.fsdb",
                        type=str,
                        help="Output pattern to split on, which should contain a PERCENT S to use for inserting the column value being saved to that file.")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="str")

    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    # open the input file
    inh = pyfsdb.Fsdb(file_handle=args.input_file)
    key_column = inh.get_column_number(args.column)

    out_handles = {}

    for row in inh:
        value = row[key_column]

        # see if we have an open file handle for this one yet
        if value not in out_handles:
            # new value, so open a new file handle to save data for it
            file_name = re.sub("[^-.0-9a-zA-Z_]", "_", str(value))
            outh = pyfsdb.Fsdb(out_file=(args.output_pattern % file_name))
            outh.column_names = inh.column_names
            out_handles[value] = outh

        # save the row to the file based on its value
        out_handles[value].append(row)

    # clean up
    for handle in out_handles:
        out_handles[handle].close()

if __name__ == "__main__":
    main()
