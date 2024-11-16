"""Find the top (bottom) N rows identified by a key and sorted by a
value column.  The result will be N rows with unique keys, sorted
by the top N value columns.

Examples:

Given a dataset like:

  #fsdb -F t one two three
  10	a	42
  20	b	99
  20	a	50

and running it as:

  topn -n 2 -k two -v three

Will produce:

  #fsdb -F t one two three
  20	b	99
  20	a	50

(ie, one row for each a and b)

Or:

  topn -n 1 -k two -v three

creates:

  #fsdb -F t one two three
  20	b	99

"""

import sys
import argparse
import pyfsdb


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__
    )

    parser.add_argument(
        "-k", "--key", default="key", type=str, help="Name of the key column to use"
    )

    parser.add_argument(
        "-v",
        "--value",
        default="value",
        type=str,
        help="Name of the value column to use when sorting",
    )

    parser.add_argument(
        "-n", "--max-rows", default=20, type=int, help="Number of rows to return"
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
    return args


def maybe_add_data(data_by_key, row, key_column, value_column, min_add_value, max_rows):
    if row[key_column] in data_by_key:
        # update the existing
        data_by_key[row[key_column]] = row
    else:
        # it's a new row, append it
        data_by_key[row[key_column]] = row
        # and maybe drop an old row
        if len(data_by_key) > max_rows:
            # need to drop the lowest, which also has min_add_value
            delete_this = min(
                data_by_key, key=lambda x: float(data_by_key[x][value_column])
            )
            del data_by_key[delete_this]

            # calculate he new minimum
            min_key = min(
                data_by_key, key=lambda x: float(data_by_key[x][value_column])
            )
            min_add_value = float(data_by_key[min_key][value_column])

    return min_add_value


def main():
    args = parse_args()

    fh = pyfsdb.Fsdb(file_handle=args.input_file, out_file_handle=args.output_file)

    (key_column, value_column) = fh.get_column_numbers([args.key, args.value])
    min_add_value = None
    data_by_key = {}
    for row in fh:
        if (
            row[value_column] is not None
            and row[value_column] != "-"
            and row[value_column] != ""
        ):
            if min_add_value is None or min_add_value < float(row[value_column]):
                min_add_value = maybe_add_data(
                    data_by_key,
                    row,
                    key_column,
                    value_column,
                    min_add_value,
                    args.max_rows,
                )
            elif row[key_column] in data_by_key and float(
                data_by_key[row[key_column]][value_column]
            ) < float(row[value_column]):
                min_add_value = maybe_add_data(
                    data_by_key,
                    row,
                    key_column,
                    value_column,
                    min_add_value,
                    args.max_rows,
                )

    for key in data_by_key:
        fh.append(data_by_key[key])


if __name__ == "__main__":
    main()
