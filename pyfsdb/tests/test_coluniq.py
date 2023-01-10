import unittest
import re
import sys


def noop():
    pass


def truncate_comments(value):
    value = re.sub("\n# +\\|.*", "", value)
    return value


class TestColUniq(unittest.TestCase):
    def test_single_uniques(self):
        from io import StringIO

        data = "#fsdb -F t a b c\na\tb\tc\nb\tc\td\na\tb\td\n"

        from pyfsdb.tools.pdbcoluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ["a"])

        # check the the result
        self.assertEqual(
            truncate_comments(outh.getvalue()),
            "#fsdb -F t a:a\na\nb\n",
            "resulting values are right from uniq",
        )

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ["a"], count=True)

        # check the the result
        self.assertEqual(
            truncate_comments(outh.getvalue()),
            "#fsdb -F t a:a count:l\na\t2\nb\t1\n",
            "resulting values are right from uniq",
        )

    def test_multi_keys(self):
        from io import StringIO

        data = "#fsdb -F t a b c\na\tb\tc\nb\tc\td\na\tb\td\n"

        from pyfsdb.tools.pdbcoluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ["a", "b"])

        # check the the result
        self.assertEqual(
            truncate_comments(outh.getvalue()),
            "#fsdb -F t a:a b:a\na\tb\nb\tc\n",
            "resulting values are right from uniq",
        )

        #
        # three columns with counting
        #
        data = "#fsdb -F t x:a y:a z:a\na\tb\tc\nb\tc\td\na\tb\td\na\tb\tc\n"

        from pyfsdb.tools.pdbcoluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ["x", "y", "z"], count=True)

        # check the the result
        self.assertEqual(
            truncate_comments(outh.getvalue()),
            "#fsdb -F t x:a y:a z:a count:l\na\tb\tc\t2\na\tb\td\t1\nb\tc\td\t1\n",
            "resulting values are right from uniq",
        )

    def test_aggregate(self):
        from io import StringIO

        data = "#fsdb -F t a b c count\na\tb\tc\t2\nb\tc\td\t4\na\tb\tc\t10\n"

        from pyfsdb.tools.pdbcoluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(
            datah, outh, ["a", "b", "c"], count=True, initial_count_key="count"
        )

        # check the the result
        output = outh.getvalue()
        self.assertEqual(
            truncate_comments(output),
            "#fsdb -F t a:a b:a c:a count:l\na\tb\tc\t12\nb\tc\td\t4\n",
            "resulting values are right from uniq",
        )
