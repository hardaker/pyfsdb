import unittest


def noop():
    pass


class TestColUniq(unittest.TestCase):
    def test_single_uniques(self):
        from io import StringIO
        data = "#fsdb -F t a b c\na\tb\tc\nb\tc\td\na\tb\td\n"

        from pyfsdb.coluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, 'a')

        # check the the result
        self.assertEqual(outh.getvalue(),
                        "#fsdb -F t a\na\nb\n#   | /usr/bin/pytest-3 pyfsdb/tests/test_coluniq.py\n",
                        "resulting values are right from uniq")

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, 'a', count=True)

        # check the the result
        self.assertEqual(outh.getvalue(),
                        "#fsdb -F t a count\na\t2\nb\t1\n#   | /usr/bin/pytest-3 pyfsdb/tests/test_coluniq.py\n",
                        "resulting values are right from uniq")

