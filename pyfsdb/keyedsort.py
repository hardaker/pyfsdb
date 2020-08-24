#!/usr/bin/python3

"""Sort "mostly sorted" large FSDB files using a double pass

dbkeyedsort reads a file twice, sorting the data by the column specified via the -c/--column option.  During the first pass, it counts all the rows per key to manage which lines it needs to memorize as it's making its second pass.  During the second pass, it only stores in memory the lines that are out of order.  This can greatly optimize the amount of memory stored when the data is already in a fairly sorted state (which is common for the output of map/reduce operations such as hadoop).  This comes at the expense of needing to read the entire dataset twice, which means its impossible to use `stdin` to pass in data; instead a filename must be specified instead.  The output, though, may be `stdout`.

USAGE

    dbkeyedsort <-c COLUMN> INPUT_FILE OUTPUT_FILE

EXAMPLE

    dbkeyedsort -c timestamp sortthis.fsdb output.fsdb

"""

import sys
import argparse
import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("-c", "--column", type=str, 
                        help="The column to sort by")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Output number of rows cached to stderr")

    parser.add_argument("input_file", type=str,
                        help="The file to read (can't be stdin; must be seekable)")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The file to write to")

    args = parser.parse_args()

    if 'column' not in args:
        raise ValueError('--column or -c is required')

    return args

def main():
    args = parse_args()

    f = pyfsdb.Fsdb(args.input_file)
    key_column = f.get_column_number(args.column)
    key_counts = {}

    line_count = 0
    cached_count = 0

    # memorize all the keys and the number of rows in each
    for row in f.next_as_array():
        line_count += 1
        if row[key_column] not in key_counts:
            key_counts[row[key_column]] = 1
        else:
            key_counts[row[key_column]] += 1

    key_list = list(key_counts.keys())
    key_list.sort()

    # re-open the input file to re-read
    f = pyfsdb.Fsdb(args.input_file, out_file_handle=args.output_file)

    stored_lines = {}

    # memorize all the keys and the number of rows in each
    current_key = key_list.pop(0)
    for row in f.next_as_array():
        if row[key_column] != current_key:
            # the current lines are arriving too early; cache them
            cached_count += 1
            if row[key_column] not in stored_lines:
                stored_lines[row[key_column]] = [row]
            else:
                stored_lines[row[key_column]].append(row)
        else:
            f.append(row)
            key_counts[current_key] -= 1

            while key_counts[current_key] == 0:
                #import pdb; pdb.set_trace()
                # we're done with this key list
                if len(key_list) == 0:
                    break # done!

                # grab a new key
                current_key = key_list.pop(0)

                # write out any cached lines
                if current_key in stored_lines:
                    for stored_row in stored_lines[current_key]:
                        f.append(stored_row)
                        key_counts[current_key] -= 1
                    del stored_lines[current_key]

    f.write_finish()

    if args.verbose:
        sys.stderr.write("cached %d/%d lines\n" % (cached_count, line_count))

if __name__ == "__main__":
    main()

