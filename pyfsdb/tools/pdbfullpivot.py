#!/bin/python3

"""dbfullpivot takes an input file with time/key/value pairs, and 
   pivots the table into a wide table with one new column per key value.

   For example, if the input was this:

       #fsdb -F s time key value
       1 foo 10
       2 bar 20
       2 foo 30
       3 bar 40

   It would convert this to:

       #fsdb -F s time foo bar
       1 10 0
       2 30 20
       3 0 40

   """

import sys
import argparse
import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="")

    parser.add_argument("-k", "--key-column", default="key", type=str,
                        help="The key to pivot around")

    parser.add_argument("-t", "--time-column", default="time", type=str,
                        help="The binned time column to use")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # set up storage structures
    storage = {}
    columns = {}

    # open the input file stream
    input = pyfsdb.Fsdb(file_handle = args.input_file)

    # from the input, get extract column numbers/names
    time_column = input.get_column_number(args.time_column)
    key_column = input.get_column_number(args.key_column)
    column_names = input.column_names

    # for each row, remember each value based on time and key
    for row in input:
        # if the time hasn't been seen before, allocate the sub-structure
        if row[time_column] not in storage:
            storage[row[time_column]] = {}

        for column_num in range(0,len(row)):
            # remember all values of non-time and non-key columns 
            if column_num != time_column and column_num != key_column:
                storage[row[time_column]][row[key_column]] = row[column_num]
                # record that we've seen this column before
                columns[row[key_column]] = 1

    # open the output stream, and set it's properties
    out = pyfsdb.Fsdb(out_file_handle = args.output_file)

    # the output columns will be a merge of the time column, and
    # previously seen key-index values.
    output_columns = ['time']
    output_columns.extend(columns.keys())
    out.out_column_names = output_columns

    # Output all data, grouped by time_key 
    for time_key in storage:

        # create a row containing a column for every seen key
        row = [time_key]
        for column in columns:
            if column not in storage[time_key] or storage[time_key][column] == "":
                row.append("0")
            else:
                row.append(storage[time_key][column])

        # write it out
        out.append(row)

    
if __name__ == "__main__":
    main()
