import pyfsdb
import unittest
from io import StringIO
from logging import error


class TestCommandParsing(unittest.TestCase):
    commands = ["command1", "command2"]
    DATA_FILE = "pyfsdb/tests/tests.fsdb"

    def test_get_commands_at_end(self):
        fh = pyfsdb.Fsdb(self.DATA_FILE)
        fh.get_all()
        read_commands = fh.commands
        self.assertEqual(self.commands, read_commands)

    def test_get_commands_before_end(self):
        fh = pyfsdb.Fsdb(self.DATA_FILE)
        read_commands = fh.commands
        self.assertEqual(self.commands, read_commands)

        # make sure we can read data too even after reading ahead
        self.assertEqual(next(fh), ["rowone", "info", "data"])
