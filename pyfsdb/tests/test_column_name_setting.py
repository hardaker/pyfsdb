import unittest
from io import StringIO
import pyfsdb


class test_column_name_setting(unittest.TestCase):
    def test_out_columns_dont_break_in_columns(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2\na 4\na\n")
        outdata = StringIO()

        with pyfsdb.Fsdb(
            file_handle=indata,
            out_file_handle=outdata,
            out_column_names=["no", "third"],
        ) as fh:
            next(fh)
            self.assertEqual(fh.column_names, ["a", "b", "c"])
            self.assertEqual(fh.out_column_names, ["no", "third"])

    def test_out_columns_set_late_dont_break_in_columns(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2\na 4\na\n")
        outdata = StringIO()

        with pyfsdb.Fsdb(file_handle=indata, out_file_handle=outdata) as fh:
            fh.out_column_names = ["no", "third"]
            next(fh)
            self.assertEqual(fh.column_names, ["a", "b", "c"])
            self.assertEqual(fh.out_column_names, ["no", "third"])

    def test_out_columns_set_later_dont_break_in_columns(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2\na 4\na\n")
        outdata = StringIO()

        with pyfsdb.Fsdb(file_handle=indata, out_file_handle=outdata) as fh:
            next(fh)
            fh.out_column_names = ["no", "third"]
            self.assertEqual(fh.column_names, ["a", "b", "c"])
            self.assertEqual(fh.out_column_names, ["no", "third"])
