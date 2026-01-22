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


def fill_values(
    fh: pyfsdb.Fsdb,
    key_column: str = "timestamp",
    columns: list[str] = [],
    value: int | float | str = 0,
    bin_size: int = 1,
    other_keys: list[str] = [],
    copy_keys: list[str] = [],
):
    store_columns = fh.get_column_numbers(columns)
    time_column = fh.get_column_number(key_column)
    other_columns = []
    if other_keys:
        other_columns = fh.get_column_numbers(other_keys)

    copy_columns = []
    if copy_keys:
        copy_columns = fh.get_column_numbers(copy_keys)

    value = value
    bin_size = bin_size

    last_index = None
    last_other_columns = set()
    last_row = None

    other_key_values = set()

    last_rows = {}

    for row in fh:
        key_set = tuple(row[x] for x in other_columns)

        if other_keys:  # save the other set of unique keys
            other_key_values.add(key_set)

        if last_index is None:
            # first row, just store it
            last_index = int(row[time_column])
        elif last_index != int(row[time_column]):
            # fill in previous time's other keys if needed
            # TODO(hardaker): implement this
            # add any entirely missing time values

            # check for partially filled rows
            # TODO(hardaker): should this go after range skipping???
            for key in last_rows:
                if key not in last_other_columns:
                    newrow = list(last_rows[key])  # duplicate the last seen
                    for column_num, col_value in zip(other_columns, key):
                        newrow[column_num] = col_value
                    newrow[time_column] = str(last_index)
                    for column in store_columns:
                        newrow[column] = value
                    fh.append(newrow)

            for skipped_time in range(
                last_index + bin_size, int(row[time_column]), bin_size
            ):
                if len(other_keys) == 0:
                    # TODO(hardaker): make last/next row to copy selectable?
                    newrow = list(last_row)  # duplicate the last_row row
                    newrow[time_column] = str(skipped_time)
                    for column in store_columns:
                        newrow[column] = value
                    fh.append(newrow)
                else:
                    for key_set in other_key_values:
                        newrow = list(last_rows[key_set])  # duplicate the current row
                        for column_num, col_value in zip(other_columns, key_set):
                            newrow[column_num] = col_value
                        newrow[time_column] = str(skipped_time)
                        for column in store_columns:
                            newrow[column] = value
                        fh.append(newrow)

            last_index = int(row[time_column])
            last_other_columns = set()

        last_other_columns.add(key_set)
        last_rows[key_set] = row
        last_row = row
        fh.append(row)

    # do a final fill for the last column
    for key in last_rows:
        if key not in last_other_columns:
            newrow = list(last_rows[key])  # duplicate the last seen
            for column_num, col_value in zip(other_columns, key):
                newrow[column_num] = col_value
            newrow[time_column] = str(last_index)
            for column in store_columns:
                newrow[column] = value
            fh.append(newrow)

    fh.close()


def main():
    args = parse_args()

    fh = pyfsdb.Fsdb(file_handle=args.input_file, out_file_handle=args.output_file)
    fill_values(
        fh,
        key_column=args.key_column,
        columns=args.columns,
        value=args.value,
        bin_size=args.bin_size,
        other_keys=args.other_keys,
    )


if __name__ == "__main__":
    main()
