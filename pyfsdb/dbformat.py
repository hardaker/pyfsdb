#!/usr/bin/python3

"""Outputs a python-string formatted line for every input FSDB row,
with column names acting as variables into the format string."""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
import sys
import pyfsdb

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
	                        epilog="Example: dbformat -f 'I can print {col1} and {col2}'")

    parser.add_argument("-f", "--format", type=str,
                        help="The python-based format string to use")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input FSDB file to read")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output text file to write to")

    args = parser.parse_args()

    if not args.format:
        sys.stderr.write("-f is a required argument\n")
        exit(1)
        
    return args

def main():
    args = parse_args()

    inh = pyfsdb.Fsdb(file_handle = args.input_file,
                      return_type=pyfsdb.RETURN_AS_DICTIONARY)
    outh= args.output_file

    format_string = args.format

    for row in inh:
        outh.write(format_string.format(**row) + "\n")

if __name__ == "__main__":
    main()
