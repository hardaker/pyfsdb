"""Fills a row that is missing in a series of rows with a numerical
increasing (frequently a timestamp) index"""

import sys
import argparse
import pyfsdb


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__
    )

    parser.add_argument(
        "-v", "--value", default="0", type=str, help="Fill columns with this value"
    )

    parser.add_argument(
        "-c", "--columns", type=str, nargs="+", help="Fill these columns"
    )

    parser.add_argument(
        "-k",
        "--key-column",
        default="timestamp",
        type=str,
        help="Use this column as the timestamp/key column to increment",
    )

    parser.add_argument(
        "-o",
        "--other-keys",
        default=[],
        nargs="*",
        type=str,
        help="Use this set of columns as other values to ensure are present per primary key column.",
    )

    parser.add_argument(
        "-b",
        "--bin-size",
        default=1,
        type=int,
        help="Bin-size to check for missing rows",
    )

    parser.add_argument(
        "input_file", type=argparse.FileType("r"), nargs="?", default=sys.stdin, help=""
    )

    parser.add_argument(
        "output_file",
        type=argparse.FileType("w"),
        nargs="?",
        default=sys.stdout,
        help="",
    )

    args = parser.parse_args()

    if args.columns is None:
        sys.stderr.write("The --columns argument is required\n")
        exit(1)

    return args


def main():
    args = parse_args()

    fh = pyfsdb.Fsdb(file_handle=args.input_file, out_file_handle=args.output_file)

    store_columns = fh.get_column_numbers(args.columns)
    time_column = fh.get_column_number(args.key_column)
    other_columns = []
    if args.other_keys:
        other_columns = fh.get_column_numbers(args.other_keys)
    value = args.value
    bin_size = args.bin_size

    last_index = None

    other_keys = set()

    for row in fh:
        if args.other_keys:  # save the other set of unique keys
            other_keys.add(tuple(row[x] for x in other_columns))
        if last_index is None:
            # first row, just store it
            last_index = int(row[time_column])
        elif last_index != int(row[time_column]):
            for skipped_time in range(
                last_index + bin_size, int(row[time_column]), bin_size
            ):
                if len(args.other_keys) == 0:
                    newrow = list(row)  # duplicate the current row
                    newrow[time_column] = str(skipped_time)
                    for column in store_columns:
                        newrow[column] = value
                    fh.append(newrow)
                else:
                    for key_set in other_keys:
                        newrow = list(row)  # duplicate the current row
                        for column_num, col_value in zip(other_columns, key_set):
                            newrow[column_num] = col_value
                        newrow[time_column] = str(skipped_time)
                        for column in store_columns:
                            newrow[column] = value
                        fh.append(newrow)

            last_index = int(row[time_column])
        fh.append(row)

    fh.close()


if __name__ == "__main__":
    main()
