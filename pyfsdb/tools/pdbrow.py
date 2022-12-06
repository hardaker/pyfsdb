"""Selects rows based on python boolean expressions"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import pyfsdb


def parse_args():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: pdbrow 'column_a == 5' input.fsdb output.fsdb",
    )

    parser.add_argument("-i", "--init-code",
                        help="Initialization code to execute first (eg, imports)")

    parser.add_argument(
        "--log-level", default="info", help="Define the logging verbosity level."
    )

    parser.add_argument(
        "expression",
        help="The boolean expression to evaluate",
    )

    parser.add_argument(
        "input_file",
        type=FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="The input FSDB file",
    )

    parser.add_argument(
        "output_file",
        type=FileType("w"),
        nargs="?",
        default=sys.stdout,
        help="Where to write the output FSDB to",
    )

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")
    return args


def process_pdbrow(
        input_file,
        output_file,
        expression,
        init_code = None,
):

    # open input and output fsdb handles
    fh = pyfsdb.Fsdb(file_handle=input_file, return_type=pyfsdb.RETURN_AS_DICTIONARY)
    oh = pyfsdb.Fsdb(out_file_handle=output_file)

    # crate output columns
    oh.out_column_names = fh.column_names

    globals = {}

    if init_code:
        exec(compile(init_code, '<string>', 'exec'), globals)

    compiled_expression = compile(f"{expression}", '<string>', 'eval')

    # process the rows
    for row in fh:

        # execute the expression and check its result
        result = eval(compiled_expression, globals, row)
        if result:
            oh.append(row)

    oh.close()

def main():
    args = parse_args()

    process_pdbrow(
        args.input_file,
        args.output_file,
        args.expression,
        args.init_code,
    )


if __name__ == "__main__":
    main()

