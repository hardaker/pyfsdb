from io import StringIO
import pyfsdb


def encode_to_fsdb(data: list[list], columns: list[str] = None) -> StringIO:
    """Take a double array and encode it to an FSDB 'file' string.

    If columns aren't specified, then letters a..z will be used."""

    if not columns:
        columns = [x for x in "abcdefghijklmnopqrstuvwxyz"]
        columns = columns[: len(data[0])]

    contents = StringIO()
    encoded: str = ""
    with pyfsdb.Fsdb(out_file_handle=contents, out_column_names=columns) as fh:
        fh.put_all(data)
        encoded = contents.getvalue()

    return encoded


def main():
    print(encode_to_fsdb([["a", 1, 2], ["b", 3, 4]]))

    print(encode_to_fsdb([["a", 1, 2], ["b", 3, 4]], columns="x foo bar".split()))


if __name__ == "__main__":
    main()
