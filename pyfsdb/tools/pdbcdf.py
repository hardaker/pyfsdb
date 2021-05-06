"""Creates a CDF fraction column from another column's data.  Note
that this requires loading all the data into memory for efficiency."""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warn, error, critical, basicConfig
import sys
import pyfsdb

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: ")

    parser.add_argument("-c", "--data-column", default="data",
                        type=str,
                        help="The input column name to create a CDF from")

    parser.add_argument("-C", "--cdf-column", default=None,
                        type=str,
                        help="The output CDF column name -- if none, '_cdf' will be appended to --column")

    parser.add_argument("-m", "--use-max", action="store_true",
                        help="Use the maximum of the data column instead of the sum to divide by")

    parser.add_argument("--log-level", default="info",
                        help="Define the logging verbosity level.")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The input FSDB file")

    parser.add_argument("output_file", type=FileType('w'),
                        nargs='?', default=sys.stdout,
                        help="Where to write the output FSDB to")

    args = parser.parse_args()
    basicConfig(level=args.log_level)
    return args

def process_cdf(input_file, output_file, data_column,
                out_cdf=None, use_max=False):
    # open input and output fsdb handles
    fh = pyfsdb.Fsdb(file_handle=input_file)
    oh = pyfsdb.Fsdb(out_file_handle=output_file)

    # crate output columns
    out_columns = fh.column_names

    if not out_cdf:
        out_cdf = data_column + "_cdf"
    
    out_columns.append(out_cdf)
    oh.out_column_names = out_columns

    df = fh.get_pandas(data_has_comment_chars=True)

    if use_max:
        denominator = df[data_column].max()
    else:
        denominator = df[data_column].sum()

    df[out_cdf] = df[data_column] / denominator

    oh.put_pandas(df)

def main():
    args = parse_args()

    process_cdf(args.input_file, args.output_file,
                args.data_column, args.cdf_column,
                args.use_max)

if __name__ == "__main__":
    main()
