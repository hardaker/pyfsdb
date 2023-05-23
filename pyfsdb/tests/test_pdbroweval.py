from io import StringIO
import unittest
import pyfsdb
import copy
from logging import error


def noop():
    pass


class test_pdbroweval(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test_pdbroweval, self).__init__(*args, **kwargs)
        self.input_data = [
            {"a": 5, "b": 10, "c": 15},
            {"a": 2, "b": 4, "c": 8},
            {"a": 3, "b": 6, "c": 9},
        ]

    def test_load(self):
        from pyfsdb.tools.pdbroweval import process_pdbroweval

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

    def base_test_and_eval(
        self,
        expression,
        expected_result,
        init_code=None,
        from_file=False,
        init_code_file=False,
        underbars=False,
    ):
        from pyfsdb.tools.pdbroweval import process_pdbroweval

        input_data_fsdb = self.get_standard_input()
        output_data = StringIO()
        output_data.close = noop

        process_pdbroweval(
            input_data_fsdb,
            output_data,
            expression,
            init_code=init_code,
            expression_is_file=from_file,
            init_code_is_file=init_code_file,
            use_underbars=underbars,
        )

        data = pyfsdb.Fsdb(
            file_handle=StringIO(output_data.getvalue()),
            return_type=pyfsdb.RETURN_AS_DICTIONARY,
        ).get_all()

        self.assertEqual(data, expected_result)

    def test_no_changes(self):
        self.base_test_and_eval("pass", self.input_data)

    def test_change_a_x_2(self):
        results = copy.deepcopy(self.input_data)
        for row in results:
            row["a"] *= 2
        self.base_test_and_eval("a *= 2", results)

    def test_change_letter_x_a(self):
        results = copy.deepcopy(self.input_data)
        for row in results:
            row["c"] = "x" * row["a"]
        self.base_test_and_eval("c = 'x' * a", results)

    def test_change_b_two_passes(self):
        results = copy.deepcopy(self.input_data)
        for row in results:
            row["b"] = str(row["a"])
            row["c"] = row["b"] * row["a"]
        self.base_test_and_eval("b = str(a); c = b * a", results)

    def test_init(self):
        import re as relonger

        results = copy.deepcopy(self.input_data)
        for row in results:
            row["b"] = relonger.sub("3", "x", str(row["a"]))
        self.base_test_and_eval("b = re.sub('3', 'x', str(a))", results, "import re")

    def test_other_var_creation(self):
        self.base_test_and_eval("d = 2", self.input_data)

    def test_filehandle_code(self):
        code = StringIO("a = 1\nb = 2\nc = 3")
        results = [{"a": 1, "b": 2, "c": 3}] * 3
        self.base_test_and_eval(code, results, from_file=True)

    def test_init_code_file(self):
        import re as relonger

        results = copy.deepcopy(self.input_data)
        for row in results:
            row["b"] = relonger.sub("3", "x", str(row["a"]))
        self.base_test_and_eval(
            "b = re.sub('3', 'x', str(a))",
            results,
            StringIO("import re"),
            init_code_file=True,
        )

    def test_underbar_names(self):
        code = StringIO("_a = 1\n_b = 2\n_c = 3")
        results = [{"a": 1, "b": 2, "c": 3}] * 3
        self.base_test_and_eval(code, results, from_file=True, underbars=True)
