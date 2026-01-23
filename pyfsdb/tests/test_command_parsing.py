import pytest
import pyfsdb
import unittest
from io import StringIO
from logging import error


@pytest.fixture
def DATA_FILE(tmp_path):
    content = """#fsdb -F t colone coltwo colthree
rowone	info	data
# middle comment
rowtwo	other	stuff
#  | command1
#   | command2
"""
    tmpfile = tmp_path / "test.fsdb"
    tmpfile.write_text(content, encoding="utf-8")
    return tmpfile


commands = ["command1", "command2"]
COMP_FILE = "pyfsdb/tests/testscomp.fsdb.xz"
test_data = "#fsdb -f s a b c\n1 2 3\n4 5 6\n# | command one"
ROW1 = ["rowone", "info", "data"]
ROW2 = ["rowtwo", "other", "stuff"]

def test_history_from_stringio_fails():
    test_file = StringIO(test_data)
    fh = pyfsdb.Fsdb(file_handle=test_file)

    history_data = fh.commands
    assert history_data is None

def test_get_commands_at_end(DATA_FILE):
    fh = pyfsdb.Fsdb(DATA_FILE)
    fh.get_all()
    read_commands = fh.commands
    assert commands == read_commands

def test_get_commands_before_end(DATA_FILE):
    fh = pyfsdb.Fsdb(DATA_FILE)
    read_commands = fh.commands
    assert next(fh) == ROW1
    assert commands == read_commands

    # make sure we can read data too even after reading ahead
    assert next(fh) == ROW2

def test_compressed_files():
    # ensure we can test thsi
    try:
        import lzma
    except Exception:
        return

    fh = pyfsdb.Fsdb(COMP_FILE)
    row = next(fh)
    assert row == ROW1

def test_command_gathering_in_compressed():
    # ensure we can test thsi
    try:
        import lzma
    except Exception:
        return

    fh = pyfsdb.Fsdb(COMP_FILE)
    row = next(fh)
    assert row == ROW1

    test_commands = fh.commands
    assert test_commands is None  # None == failure to read

    row = next(fh)
    assert row == ROW2
