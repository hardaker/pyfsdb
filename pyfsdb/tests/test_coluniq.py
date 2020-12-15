import unittest


def noop():
    pass


class TestColUniq(unittest.TestCase):
    def test_single_uniques(self):
        from io import StringIO
        data = "#fsdb -F t a b c\na\tb\tc\nb\tc\td\na\tb\td\n"

        from pyfsdb.dbcoluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ['a'])

        # check the the result
        self.assertEqual(outh.getvalue(),
                        "#fsdb -F t a\na\nb\n#   | /usr/bin/pytest-3 pyfsdb/tests/test_coluniq.py\n",
                        "resulting values are right from uniq")

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ['a'], count=True)

        # check the the result
        self.assertEqual(outh.getvalue(),
                        "#fsdb -F t a count\na\t2\nb\t1\n#   | /usr/bin/pytest-3 pyfsdb/tests/test_coluniq.py\n",
                        "resulting values are right from uniq")


    def test_multi_keys(self):
        from io import StringIO
        data = "#fsdb -F t a b c\na\tb\tc\nb\tc\td\na\tb\td\n"

        from pyfsdb.dbcoluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ['a', 'b'])

        # check the the result
        self.assertEqual(outh.getvalue(),
                        "#fsdb -F t a b\na\tb\nb\tc\n#   | /usr/bin/pytest-3 pyfsdb/tests/test_coluniq.py\n",
                        "resulting values are right from uniq")


        #
        # three columns with counting
        #
        data = "#fsdb -F t x y z\na\tb\tc\nb\tc\td\na\tb\td\na\tb\tc\n"

        from pyfsdb.dbcoluniq import filter_unique_columns

        outh = StringIO()
        outh.close = noop
        datah = StringIO(data)
        filter_unique_columns(datah, outh, ['x', 'y', 'z'], count=True)

        # check the the result
        self.assertEqual(outh.getvalue(),
                        "#fsdb -F t x y z count\na\tb\tc\t2\na\tb\td\t1\nb\tc\td\t1\n#   | /usr/bin/pytest-3 pyfsdb/tests/test_coluniq.py\n",
                        "resulting values are right from uniq")

