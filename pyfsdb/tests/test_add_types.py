import unittest
from io import StringIO
from pyfsdb.tools.pdbaddtypes import add_types
from unittest.mock import Mock
from test_fsdb_class import truncate_comments


class test_add_types(unittest.TestCase):
    def test_add_single_type(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2.3")
        outdata = StringIO()
        outdata.close = Mock()
        add_types(indata, outdata, ["b=l"])
        self.assertEqual(
            truncate_comments(outdata.getvalue()), "#fsdb -F s a b:l c\na 1 2.3"
        )

    def test_add_multiple_types(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2.3")
        outdata = StringIO()
        outdata.close = Mock()
        add_types(indata, outdata, ["b=l", "c=d"])
        self.assertEqual(
            truncate_comments(outdata.getvalue()), "#fsdb -F s a b:l c:d\na 1 2.3"
        )

    def test_merge_types(self):
        indata = StringIO("#fsdb -F s a b:l c\na 1 2.3")
        outdata = StringIO()
        outdata.close = Mock()
        add_types(indata, outdata, ["c=d"])
        self.assertEqual(
            truncate_comments(outdata.getvalue()), "#fsdb -F s a b:l c:d\na 1 2.3"
        )

    def test_override_types(self):
        indata = StringIO("#fsdb -F s a b:l c:d\na 1 2.3")
        outdata = StringIO()
        outdata.close = Mock()
        add_types(indata, outdata, ["b=d"])
        self.assertEqual(
            truncate_comments(outdata.getvalue()), "#fsdb -F s a b:d c:d\na 1 2.3"
        )

    def test_guess_converters(self):
        import pyfsdb

        indata = StringIO("#fsdb -F s a b c\na 1 2.3")
        f = pyfsdb.Fsdb(file_handle=indata, return_type=pyfsdb.RETURN_AS_DICTIONARY)
        row = next(f)
        self.assertEqual(row, {"a": "a", "b": "1", "c": "2.3"})

        converters = f.guess_converters(row)
        self.assertEqual(converters, {"b": int, "c": float})

    def test_auto_convert(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2.3")
        outdata = StringIO()
        outdata.close = Mock()
        add_types(indata, outdata, auto_convert=True)
        self.assertEqual(
            truncate_comments(outdata.getvalue()), "#fsdb -F s a b:l c:d\na 1 2.3"
        )

    def test_auto_convert_overrides(self):
        indata = StringIO("#fsdb -F s a b c\na 1 2.3")
        outdata = StringIO()
        outdata.close = Mock()
        add_types(indata, outdata, types=["b=d"], auto_convert=True)
        self.assertEqual(
            truncate_comments(outdata.getvalue()), "#fsdb -F s a b:d c:d\na 1 2.3"
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
