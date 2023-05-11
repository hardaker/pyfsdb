"""Modifies rows based on python code passed as an expression (or file)"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import pyfsdb


def get_parse_args():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: pdbroweval 'column_a = column_a * 5' input.fsdb output.fsdb",
    )

    parser.add_argument(
        "-u",
        "--underbars",
        action="store_true",
        help="Use variable names with _ prefixes to the column names",
    )

    parser.add_argument(
        "-i", "--init-code", help="Initialization code to execute first (eg, imports)"
    )

    parser.add_argument(
        "-f",
        "--expression-is-file",
        action="store_true",
        help="The expression is actually a python code file to load",
    )

    parser.add_argument(
        "-I",
        "--init-code-is-file",
        action="store_true",
        help="The expression is actually a python code file to load",
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

    return parser


def parse_args():
    parser = get_parse_args()
    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")
    return args


def process_pdbroweval(
    input_file,
    output_file,
    expression,
    init_code=None,
    expression_is_file=False,
    init_code_is_file=False,
    use_underbars=False,
):

    # open input and output fsdb handles
    fh = pyfsdb.Fsdb(file_handle=input_file, return_type=pyfsdb.RETURN_AS_DICTIONARY)
    oh = pyfsdb.Fsdb(out_file_handle=output_file)

    # crate output columns
    oh.out_column_names = fh.column_names

    globals = {}

    if init_code:
        if init_code_is_file:
            init_code = init_code.read()
        exec(compile(init_code, "<string>", "exec"), globals)

    if expression_is_file:
        expression = expression.read()
        error(expression)
    compiled_expression = compile(f"{expression}", "<string>", "exec")

    # if they wanted under-bar based names
    if use_underbars:
        fh.column_names = ["_" + x for x in fh.column_names]
        fh.converters = {"_" + x: y for x, y in fh.converters.items()}

    # process the rows
    for row in fh:

        # execute the expression and check its result
        exec(compiled_expression, globals, row)
        if use_underbars:
            row = {k[1:]: v for k, v in row.items()}
        oh.append(row)

    oh.close()


def main():
    args = parse_args()

    process_pdbroweval(
        args.input_file,
        args.output_file,
        expression=args.expression,
        init_code=args.init_code,
        expression_is_file=args.expression_is_file,
        init_code_is_file=args.init_code_is_file,
        use_underbars=args.underbars,
    )


if __name__ == "__main__":
    main()
