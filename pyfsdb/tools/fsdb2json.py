#!/usr/bin/python3

"""Converts an FSDB file to a stream of json dictionaries."""

import sys
import argparse
import json
import pyfsdb

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

    parser.add_argument("-a", "--array", action="store_true",
                        help="Format the output as a large array.")

    parser.add_argument("-d", "--dictionary", type=str,
                        help="Turn the results into a json dictionary with a key from this column")

    parser.add_argument("-v", "--value", type=str,
                        help="If a dictionary out put is requested, rather than placing the entire row as the dictionary value, use just this column istead")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input file (FSDB file) to read")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output file (json file) to write back out")

    args = parser.parse_args()
    return args


def fsdb_to_json(input_file, output_file, as_array=False, as_dictionary=None, with_value=None):
    "Converts an FSDB file to a stream of json dictionary records"
    in_fsdb = pyfsdb.Fsdb(file_handle=input_file,
                          return_type=pyfsdb.RETURN_AS_DICTIONARY)

    end_token = ""
    close_token = ""
    if as_array:
        output_file.write("[")
        end_token = ","
        close_token = "]"
    if as_dictionary:
        output_file.write("{")
        end_token = ","
        close_token = "}"

    previous_record = None
    for record in in_fsdb:
        if previous_record:
            if as_dictionary:
                if with_value:
                    output_file.write(f'"{previous_record[as_dictionary]}": {json.dumps(previous_record[with_value])}{end_token}' + "\n")
                else:
                    output_file.write(f'"{previous_record[as_dictionary]}": {json.dumps(previous_record)}{end_token}' + "\n")
            else:
                output_file.write(json.dumps(previous_record) + end_token + "\n")
        previous_record = record

    if previous_record:
        if as_dictionary:
            if with_value:
                    output_file.write(f'"{previous_record[as_dictionary]}": {json.dumps(previous_record[with_value])}{close_token}' + "\n")
            else:
                output_file.write(f'"{previous_record[as_dictionary]}": {json.dumps(previous_record)}{close_token}' + "\n")
        else:
            output_file.write(json.dumps(previous_record) + close_token + "\n")

def main():
    "CLI wrapper around fsdb_to_json"
    args = parse_args()
    fsdb_to_json(args.input_file, args.output_file,
                 as_array = args.array,
                 as_dictionary = args.dictionary,
                 with_value=args.value)


if __name__ == "__main__":
    main()
