#!/usr/bin/python3

"""db2tex converts any FSDB file into a latex table.
WARNING: very little escaping is done -- watch out for mallicious input files."

import argparse
import sys
import pyfsdb

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=__doc__,
                                     epilog="Exmaple Usage: db2tex -c col1 col2 -p cc input.fsdb")

    parser.add_argument("-p", "--tabular-profile", type=str,
                        help="The column profile to pass to tabular.  The default will be all 'l's.")

    parser.add_argument("-c", "--columns", type=str, nargs="*",
                        help="Column names to include; will use all if not specified")

    parser.add_argument("-C", "--caption", type=str,
                        help="Use this as the caption for the table")

    parser.add_argument("-l", "--label", type=str,
                        help="Add a label to the table (eg: tab:foo)")

    parser.add_argument("input_file", type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input FSDB file")

    parser.add_argument("output_file", type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="The output file to print latex table data to")

    args = parser.parse_args()
    return args

def latex_escape(value):
    return str(value).replace("\\","\\\\").replace("_", "\\_").replace("&","\\&")

def main():
    args = parse_args()

    inh = pyfsdb.Fsdb(file_handle = args.input_file)
    outh = args.output_file

    columns = args.columns
    if not columns:
        columns = inh.column_names

    if args.tabular_profile:
        specifier = args.tabular_profile
    else:
        specifier = "l" * len(columns)

    column_numbers = inh.get_column_numbers(columns)

        

    # write out the header info
    outh.write("\\begin{table}\n")
    outh.write("  \\begin{tabular}{%s}\n" % (specifier))

    for num, column in enumerate(columns):
        if num == 0:
            outh.write("    \\textbf{%s}" % (latex_escape(column)))
        else:
            outh.write(" & \\textbf{%s}" % (latex_escape(column)))
    outh.write(" \\\\\n")

    for row in inh:
        for num, column in enumerate(column_numbers):
            if num == 0:
                outh.write("    %s" % (latex_escape(row[column])))
            else:
                outh.write(" & %s" % (latex_escape(row[column])))
        outh.write(" \\\\\n")


    outh.write("  \\end{tabular}\n")
    if args.caption:
        outh.write("  \\caption{%s}\n" % (args.caption))
    if args.label:
        outh.write("  \\label{%s}\n" % (args.label))
    outh.write("\\end{table}\n")

if __name__ == "__main__":
    main()
