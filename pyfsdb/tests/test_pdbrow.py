from io import StringIO
import unittest
import pyfsdb
from logging import error


def noop():
    pass


class test_pdbrow(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test_pdbrow, self).__init__(*args, **kwargs)
        self.input_data = [
            {"a": 5, "b": 10, "c": 15},
            {"a": 2, "b": 4, "c": 8},
            {"a": 3, "b": 6, "c": 9},
        ]

    def test_load(self):
        from pyfsdb.tools.pdbrow import process_pdbrow

        self.assertTrue(True, "could load")

    def convert_to_stringio(self, data):
        outh = StringIO()
        outh.close = noop
        oh = pyfsdb.Fsdb(out_file_handle=outh)
        oh.out_column_names = list(data[0].keys())
        for row in data:
            oh.append(list(row.values()))
        oh.close()
        return StringIO(outh.getvalue())

    def get_standard_input(self):
        return self.convert_to_stringio(self.input_data)

    def base_test_and_assert(
        self,
        expression,
        expected_result,
        init_code=None,
        use_underbars=False,
        use_namedtuple=None,
    ):
        from pyfsdb.tools.pdbrow import process_pdbrow

        input_data_fsdb = self.get_standard_input()
        output_data = StringIO()
        output_data.close = noop

        process_pdbrow(
            input_data_fsdb,
            output_data,
            expression,
            init_code=init_code,
            use_underbars=use_underbars,
            use_namedtuple=use_namedtuple,
        )

        data = pyfsdb.Fsdb(
            file_handle=StringIO(output_data.getvalue()),
            return_type=pyfsdb.RETURN_AS_DICTIONARY,
        ).get_all()

        self.assertEqual(data, expected_result)

    def test_true_filtering(self):
        self.base_test_and_assert("True", self.input_data)

    def test_filtering_equality(self):
        # result should be a slice of element 1
        self.base_test_and_assert("a == 2", self.input_data[1:2])

    def test_filtering_multiplication(self):
        # result should be a slice of elements 0 and 2
        self.base_test_and_assert("c == a*3", [self.input_data[0], self.input_data[2]])

    def test_filtering_math(self):
        # result should be a slice of element 1
        self.base_test_and_assert("c == a*a*a", self.input_data[1:2])

    def test_filtering_logic(self):
        # result should be a slice of elements 0 and 2
        self.base_test_and_assert(
            "c == a*3 and b == a*2", [self.input_data[0], self.input_data[2]]
        )

    def test_filtering_logic_underbars(self):
        # result should be a slice of elements 0 and 2
        self.base_test_and_assert(
            "_c == _a*3 and _b == _a*2",
            [self.input_data[0], self.input_data[2]],
            use_underbars=True,
        )

    def test_regex(self):
        # result should be a slice of elements 0 and 2
        self.base_test_and_assert(
            "re.match('3', str(a))", [self.input_data[2]], "import re"
        )

    def test_defun(self):
        # result should be a slice of elements 0 and 2
        self.base_test_and_assert(
            "testfun(a)", [self.input_data[2]], "def testfun(x):\n  return x == 3"
        )

    def test_by_namedtupel(self):
        self.base_test_and_assert(
            "row.c == row.a * 3 and row.b == row.a * 2",
            [self.input_data[0], self.input_data[2]],
            use_namedtuple="row",
        )
