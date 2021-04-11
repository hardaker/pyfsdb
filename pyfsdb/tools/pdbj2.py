#!/usr/bin/python3

"""This script takes all the data in a file, and passes it to a
   jinja2 template with each row being stored in a `rows` variable.

   Note: all the rows must be loaded into memory at once.
"""

import argparse
import sys
import os

import pyfsdb
import jinja2

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__, epilog="Example: pdbj2 -j report.j2 input.fsdb output.txt")

    parser.add_argument("-j", "--jinja2-template",
                        type=argparse.FileType('r'),
                        help="The jinja2 template file to use")

    parser.add_argument("-i", "--include-file-path", type=str,
                        help="Path to allow including files from")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs="?", default=sys.stdin,
                        help="The input file to use")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Where to write the results to")

    args = parser.parse_args()

    if not args.jinja2_template:
        sys.stderr.write("A jinja2 template argument (-j) is required\n")
        exit(1)

    return args


def process(input_file_handle, jinja2_template, output_file_handle,
            include_file_path=None):
    "Process an input data file file and template into an output file"
    # load the data
    inh = pyfsdb.Fsdb(file_handle=input_file_handle,
                      return_type=pyfsdb.RETURN_AS_DICTIONARY)
    rows = inh.get_all()

    # get jinja2 setup
    jinja_template_data = jinja2_template.read()
    loader = None

    # allowing including of other files?
    if include_file_path:
        if include_file_path[-1] != "/":
            include_file_path += "/"   # think required?
        loader = jinja2.FileStreamLoader(include_file_path)

    # create the actual template
    template = jinja2.Environment(loader=loader)
    template = template.from_string(jinja_template_data)

    # call j2 and write the results out to the file
    output_file_handle.write(template.render({'rows': rows}))


def main():
    args = parse_args()
    process(args.input_file, args.jinja2_template, args.output_file)


if __name__ == "__main__":
    main()

