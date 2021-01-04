#!/usr/bin/python3

"""dbsum will take two matricies in FSDB and add the data together
based on particular keys.  This is similar to joining and then merging
the columns, but in one application without the need to specify column
renaming/etc with otherwise identically formatted files.

Note: this requires memory large enough to store the final results in
memory at once.
""" 

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys
import pyfsdb


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: dbsum -k colone -o output.fsdb input1.fsdb input2.fsdb ...")

    parser.add_argument("-k", "--keys", default=["key"], nargs="*",
                        type=str,
                        help="Keys to use for selecting columns to add")

    parser.add_argument("-c", "--columns", default=["value"], nargs="*",
                        help="Value columns to add together")

    parser.add_argument("-s", "--subtract", action="store_true",
                        help="Subtract the other files from the first")

    parser.add_argument("-o", "--output-file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Where to save the data to")

    parser.add_argument("input_files", type=FileType('r'),
                        nargs='+', default=sys.stdin,
                        help="Input files to read from")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    data = {}
    keys = args.keys
    values = args.columns
    subtract = args.subtract

    first_file = True

    for input_file in args.input_files:
        with pyfsdb.Fsdb(file_handle=input_file,
                         return_type=pyfsdb.RETURN_AS_DICTIONARY) as fh:
            for row in fh:
                # loop through the keys and find the right deep tree spot
                ptr = data
                for key in keys:
                    if row[key] not in ptr:
                        ptr[row[key]] = {}
                    ptr = ptr[row[key]]

                # for each column, add it or subtract it from the results
                for value in values:
                    if value not in ptr:
                        ptr[value] = 0

                    if subtract and not first_file:
                        ptr[value] -= float(row[value])
                    else:
                        ptr[value] += float(row[value])
        first_file = False

    # save the output
    oh = pyfsdb.Fsdb(out_file_handle=args.output_file)
    oh.out_column_names = keys + values

    def write_recursive(spot, depth, indexes):
        if depth == 0:
            oh.append(indexes + list(spot.values()))
        else:
            for keyvalue in spot:
                write_recursive(spot[keyvalue], depth-1, indexes + [keyvalue])

    write_recursive(data, len(keys), [])


if __name__ == "__main__":
    main()

