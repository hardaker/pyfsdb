import pyfsdb
import unittest
from io import StringIO
from logging import error


class TestCommandParsing(unittest.TestCase):
    data = "#fsdb -F s a b c\n1 2 3\n4 5 6\n#  | command1\n#  | command2"
    strio = StringIO(data)
    commands = ["command1", "command2"]

    def test_get_commands_at_end(self):
        fh = pyfsdb.Fsdb(file_handle=self.strio)
        fh.get_all()
        read_commands = fh.commands
        self.assertEqual(self.commands, read_commands)
