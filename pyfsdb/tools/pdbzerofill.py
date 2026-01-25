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


def fill_row(
    time_column,
    keys,
    last_time_index,
    last_rows,
    other_key_colnums,
    store_columns,
    value,
):
    """creates a single new row from fill and past data."""
    # this key was not seen in the last set of rows, so add it now
    # which we do by duplicating the last seen row of this key_set
    newrow = list(last_rows[keys])

    # copy in the stored values for this keyset
    for column_num, key_value in zip(other_key_colnums, keys):
        newrow[column_num] = key_value

    # copy in the last time index column this key missed
    newrow[time_column] = str(last_time_index)

    # now copy in the "zero" or other value to the data columns
    for column in store_columns:
        newrow[column] = value

    return newrow


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
    other_key_colnums = []
    if other_keys:
        other_key_colnums = fh.get_column_numbers(other_keys)

    value = value
    bin_size = bin_size

    last_time_index = None

    last_other_columns = set()  # stores keys seen during this timestamp
    last_rows = {}  # stores the last row for all keys ever seen

    for row in fh:
        # note: if there are none, it'll be an empty tuple and that's ok
        key_set = tuple(row[x] for x in other_key_colnums)

        if last_time_index is None:
            # this is the very first row, so just store the first timestamp
            last_time_index = int(row[time_column])
        elif last_time_index != int(row[time_column]):
            # first: check for partially filled rows from the previous time index
            for keys in last_rows:
                if keys not in last_other_columns:
                    # this key was not seen in the last set of rows, so add it now
                    # which we do by duplicating the last seen row of this key_set
                    newrow = fill_row(
                        time_column,
                        keys,
                        last_time_index,
                        last_rows,
                        other_key_colnums,
                        store_columns,
                        value,
                    )

                    # finally, save it
                    fh.append(newrow)

            # second: fill in entirely missing rows if we did multiple time jumps forward
            for skipped_time in range(
                last_time_index + bin_size, int(row[time_column]), bin_size
            ):
                for keys in last_rows:
                    newrow = fill_row(
                        time_column,
                        keys,
                        skipped_time,
                        last_rows,
                        other_key_colnums,
                        store_columns,
                        value,
                    )
                    fh.append(newrow)

            last_time_index = int(row[time_column])
            last_other_columns = set()

        last_other_columns.add(key_set)
        last_rows[key_set] = row
        fh.append(row)

    # do a final fill for the last column
    for keys in last_rows:
        if keys not in last_other_columns:
            newrow = fill_row(
                time_column,
                keys,
                last_time_index,
                last_rows,
                other_key_colnums,
                store_columns,
                value,
            )
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
