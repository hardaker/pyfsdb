#!/usr/bin/python3

"""Converts a bro (zeek) log to a file readable by FSDB.
   Bro logs are already tab separated, so we really just replace
   the headers and re-print the rest.  brotofsdb assumes
   the bro log is properly formatted (ie, tab separated already)."""

import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("-l", "--leave-bro-headers", action="store_true",
                        help="Leave the bro headers in place right after the new FSDB header")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file (bro log) to read")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output file (FSDB log) to write back out")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    leave_headers = []

    # read in all the headers, looking for certain things
    column_names = []
    for line in args.input_file:
        if line[0] != "#":
            break


        if args.leave_bro_headers:
            leave_headers.append(line)

        if line[0:7] == "#fields":
            column_names = line.replace(".", "_").split("\t")
            column_names.pop(0)

    # print out the FSDB header
    args.output_file.write("#fsdb -F t " + " ".join(column_names))

    # optionally add back in the bro headers
    if args.leave_bro_headers:
        args.output_file.write("".join(leave_headers))

    # copy out the rest of thefile
    args.output_file.write(line)
    for line in args.input_file:
        args.output_file.write(line)

    # append our trailing command
    args.output_file.write("# " + sys.argv[0] + "\n")
    
        
if __name__ == "__main__":
    main()
