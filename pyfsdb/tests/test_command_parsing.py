import pyfsdb
import unittest
from io import StringIO
from logging import error


class TestCommandParsing(unittest.TestCase):
    commands = ["command1", "command2"]
    DATA_FILE = "pyfsdb/tests/tests.fsdb"
    COMP_FILE = "pyfsdb/tests/testscomp.fsdb.xz"
    test_data = "#fsdb -f s a b c\n1 2 3\n4 5 6\n# | command one"
    ROW1 = ["rowone", "info", "data"]
    ROW2 = ["rowtwo", "other", "stuff"]

    def test_history_from_stringio_fails(self):
        test_file = StringIO(self.test_data)
        fh = pyfsdb.Fsdb(file_handle=test_file)

        history_data = fh.commands
        self.assertEqual(history_data, None)

    def test_get_commands_at_end(self):
        fh = pyfsdb.Fsdb(self.DATA_FILE)
        fh.get_all()
        read_commands = fh.commands
        self.assertEqual(self.commands, read_commands)

    def test_get_commands_before_end(self):
        fh = pyfsdb.Fsdb(self.DATA_FILE)
        read_commands = fh.commands
        self.assertEqual(next(fh), self.ROW1)
        self.assertEqual(self.commands, read_commands)

        # make sure we can read data too even after reading ahead
        self.assertEqual(next(fh), self.ROW2)

    def test_compressed_files(self):
        # ensure we can test thsi
        try:
            import lzma
        except Exception:
            return

        fh = pyfsdb.Fsdb(self.COMP_FILE)
        row = next(fh)
        self.assertEqual(row, self.ROW1)

    def test_command_gathering_in_compressed(self):
        # ensure we can test thsi
        try:
            import lzma
        except Exception:
            return

        fh = pyfsdb.Fsdb(self.COMP_FILE)
        row = next(fh)
        self.assertEqual(row, self.ROW1)

        test_commands = fh.commands
        self.assertEqual(test_commands, None)  # None == failure to read

        row = next(fh)
        self.assertEqual(row, self.ROW2)
