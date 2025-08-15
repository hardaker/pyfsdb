import unittest
from io import StringIO
import pyfsdb


class test_missing_columns(unittest.TestCase):
    def test_fill_nones_expected(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2\na 4\na\n")

        with pyfsdb.Fsdb(file_handle=indata) as fh:
            row = next(fh)
            self.assertEqual(row, ["a", "1", "2"])

            row = next(fh)
            self.assertEqual(row, ["a", "4", ""])

            row = next(fh)
            self.assertEqual(row, ["a", "", ""])
