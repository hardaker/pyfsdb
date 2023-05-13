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

    parser.add_argument(
        "-u",
        "--underbars",
        action="store_true",
        help="Use variable names with _ prefixes to the column names",
    )

    parser.add_argument(
        "-n",
        "--namedtuple",
        default=None,
        type=str,
        help="Use a namedtuple under this name to store data",
    )

    parser.add_argument(
        "-i", "--init-code", help="Initialization code to execute first (eg, imports)"
    )

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
    init_code=None,
    use_underbars=False,
    use_namedtuple=None,
):

    return_type = pyfsdb.RETURN_AS_DICTIONARY
    if use_namedtuple:
        return_type = pyfsdb.RETURN_AS_ARRAY

    # open input and output fsdb handles
    fh = pyfsdb.Fsdb(file_handle=input_file, return_type=return_type)
    oh = pyfsdb.Fsdb(out_file_handle=output_file)

    # crate output columns
    oh.out_column_names = fh.column_names

    globals = {}

    if init_code:
        exec(compile(init_code, "<string>", "exec"), globals)

    compiled_expression = compile(f"{expression}", "<string>", "eval")

    if use_namedtuple:
        from collections import namedtuple

        named_row = namedtuple("named_row", fh.column_names)

    # process the rows
    for row in fh:

        # if they wanted under-bar based names, add them
        if use_underbars:
            result = eval(
                compiled_expression, globals, {"_" + k: v for k, v in row.items()}
            )

        elif use_namedtuple:
            contents = named_row(*row)
            result = eval(compiled_expression, globals, {use_namedtuple: contents})

        else:
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
        args.underbars,
        args.namedtuple,
    )


if __name__ == "__main__":
    main()
