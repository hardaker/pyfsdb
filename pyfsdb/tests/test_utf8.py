import pytest
import pyfsdb
from io import StringIO


DATA = "#fsdb -F t test:i copy©:i foo:a\n1\t2\t3\n4\t5\t©\n"


@pytest.fixture
def create_file(tmp_path):
    tmp_file = tmp_path / "test.fsdb"
    fh = open(tmp_file, "wb")
    fh.write(bytes(DATA, "utf-8"))
    fh.close()
    yield tmp_file


def do_test_utf8_file_handle(fh):
    row = next(fh)
    assert fh.column_names == ["test", "copy©", "foo"]
    assert row == [1, 2, "3"]

    row = next(fh)
    assert row == [4, 5, "©"]


def test_utf8_support_stringio():
    DATA_stream = StringIO(DATA)
    fh = pyfsdb.Fsdb(file_handle=DATA_stream)
    do_test_utf8_file_handle(fh)


def test_utf8_support_file(create_file):
    fh = pyfsdb.Fsdb(create_file)
    do_test_utf8_file_handle(fh)


def test_utf8_creation(tmp_path):
    tmp_file = tmp_path / "test-write.fsdb"
    fh = pyfsdb.Fsdb(out_file=tmp_file)
    fh.out_column_names = ["test", "copy©", "foo"]
    fh.append([4, 5, "©"])
    fh.close()
