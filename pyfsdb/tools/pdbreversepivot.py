#!/bin/python3

"""dbreversepivot takes an input file with time/value columns, and 
   pivots the table into a narrow table with one line per old column.

   For example, if the input was this:

       #fsdb -F s time foo bar
       1 10 0
       2 30 20
       3 0 40

   It would convert this to:

       #fsdb -F s time key value
       1 foo 10
       2 bar 20
       2 foo 30
       3 bar 40

   This is the inverse operation of dbfullpivot.
   """

import sys
import argparse
import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("-k", "--key-column", default="key", type=str,
                        help="The key column to use in the output for column names to store in")

    parser.add_argument("-c", "--columns", nargs="+", type=str,
                        help="The columns to pivot into keys")

    parser.add_argument("-v", "--value-column", default="value", type=str,
                        help="What output column to store the value for what was found in the columns")

    parser.add_argument("-o", "--other-columns", default=[], type=str, nargs="*",
                        help="Other columns to copy to every row")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input FSDB file to read")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output FSDB file to write to")


    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # set up storage structures
    storage = {}
    columns = {}

    # from the input, get extract column numbers/names
    key_column = args.key_column
    value_column = args.value_column
    other_columns = args.other_columns
    columns = args.columns

    # open the input file stream
    input = pyfsdb.Fsdb(file_handle = args.input_file,
                        return_type=pyfsdb.RETURN_AS_DICTIONARY)
    output = pyfsdb.Fsdb(out_file_handle = args.output_file)
    output.out_column_names = [key_column, value_column] + other_columns

    # for each row, remember each value based on time and key
    for row in input:
        for column in columns:
            out_row = [column, row[column]]
            for other in other_columns:
                out_row.append(row[other])
            output.append(out_row)

    output.close()
    
if __name__ == "__main__":
    main()
