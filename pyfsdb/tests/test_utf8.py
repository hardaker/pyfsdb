import pyfsdb
from io import StringIO


def do_test_utf8_file_handle(fh):
    row = next(fh)
    assert fh.column_names == ["test", "copy©", "foo"]
    assert row == [1, 2, "3"]

    row = next(fh)
    assert row == [4, 5, "©"]


def test_utf8_support():
    DATA = "#fsdb -F t test:i copy©:i foo:a\n1\t2\t3\n4\t5\t©\n"

    DATA_stream = StringIO(DATA)
    fh = pyfsdb.Fsdb(file_handle=DATA_stream)
    do_test_utf8_file_handle(fh)
