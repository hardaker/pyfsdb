import pyfsdb
from io import StringIO


def test_utf8_support():
    DATA = "#fsdb -F t test:i copy©:c foo:i\n1	2	3\n"

    DATA_stream = StringIO(DATA)
    fh = pyfsdb.Fsdb(file_handle=DATA_stream)
    row = next(fh)
    assert fh.column_names == ["test", "copy©", "foo"]
    assert row == [1, 2, 3]
