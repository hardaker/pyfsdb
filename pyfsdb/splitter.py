#!/usr/bin/python3

"""Splits a single FSDB file into multiple files."""

import argparse
import sys
import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("-c", "--columns", type=str, nargs="*",
                        help="Columns to use when splitting the file.  If not specified, all columns are split individually.  If specified, multiple columns per file can be specified using comma separated COL1,COL2 column groupings.")

    parser.add_argument("-k", "--columns-to-keep", type=str, nargs="*",
                        help="Columns to keep in every file (timestamps, keys, etc)")

    parser.add_argument("-o", "--output-file-format", default="fsdb-split-%s.fsdb", type=str,
                        help="The output file format to use.  It should contain a percent s in it, which will be replaced by the column name being split (with commas from -c being replaced by _s).")

    parser.add_argument("-b", "--write-blanks", action="store_true",
                        help="Write out blank values as well; normally data is only written when primary columns are non-blank.")



    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input FSDB file to split")


    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    input_f = pyfsdb.Fsdb(file_handle = args.input_file)

    if args.columns:
        column_names = args.columns
    else:
        column_names = input_f.column_names

    if args.columns_to_keep:
        keep_column_numbers = input_f.get_column_numbers(args.columns_to_keep)
    else:
        args.columns_to_keep = []
        keep_column_numbers = []

    split_handles = {}
    for col in column_names:
        if col in args.columns_to_keep:
            continue

        sub_columns = col.split(",")
        file_column_list = "_".join(sub_columns)

        out_column_names = []
        out_column_names.extend(args.columns_to_keep)
        out_column_names.extend(sub_columns)

        out_column_numbers = []
        out_column_numbers.extend(keep_column_numbers)
        out_column_numbers.extend(input_f.get_column_numbers(sub_columns))

        split_handles[file_column_list] = {
            "f": pyfsdb.Fsdb(out_file = (args.output_file_format % file_column_list)),
            "out_column_numbers": out_column_numbers,
            "out_column_names": out_column_names,
            "out_column_check_colnums": input_f.get_column_numbers(sub_columns),
        }
        split_handles[file_column_list]['f'].out_column_names = out_column_names

    for row in input_f.next_as_array():
        for outcol in split_handles:

            newrow = []

            # make sure we're not writing blank rows
            if not args.write_blanks:
                appends = False
                for col in split_handles[outcol]['out_column_check_colnums']:
                    if row[col] != "":
                        appends = True

                if not appends:
                    continue

            # add the existing logs
            for colnum in split_handles[outcol]['out_column_numbers']:
                newrow.append(row[colnum])
                    
            split_handles[outcol]['f'].append(newrow)


if __name__ == "__main__":
    main()
