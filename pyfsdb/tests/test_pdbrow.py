from io import StringIO
import unittest
import pyfsdb
from logging import error

def noop():
    pass

class test_pdbrow(unittest.TestCase):
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
        self.input_data = [
            {'a': 5, 'b': 10, 'c': 15},
            {'a': 2, 'b': 4, 'c': 8},
            {'a': 3, 'b': 6, 'c': 9},            
        ]
        return self.convert_to_stringio(self.input_data)

    def test_true_filtering(self):
        from pyfsdb.tools.pdbrow import process_pdbrow

        input_data_fsdb = self.get_standard_input()
        output_data = StringIO()
        output_data.close = noop

        process_pdbrow(input_data_fsdb, output_data, "True")
        
        data = pyfsdb.Fsdb(file_handle=StringIO(output_data.getvalue()),
                           return_type=pyfsdb.RETURN_AS_DICTIONARY).get_all()

        assert data == self.input_data

    def test_filtering_equality(self):
        from pyfsdb.tools.pdbrow import process_pdbrow

        input_data_fsdb = self.get_standard_input()
        output_data = StringIO()
        output_data.close = noop

        process_pdbrow(input_data_fsdb, output_data, "a == 2")
    
        data = pyfsdb.Fsdb(file_handle=StringIO(output_data.getvalue()),
                           return_type=pyfsdb.RETURN_AS_DICTIONARY).get_all()

        # result should be a slice of element 1
        assert data == self.input_data[1:2]

    def test_filtering_multiplication(self):
        from pyfsdb.tools.pdbrow import process_pdbrow

        input_data_fsdb = self.get_standard_input()
        output_data = StringIO()
        output_data.close = noop

        process_pdbrow(input_data_fsdb, output_data, "c == a*3")
    
        data = pyfsdb.Fsdb(file_handle=StringIO(output_data.getvalue()),
                           return_type=pyfsdb.RETURN_AS_DICTIONARY).get_all()

        # result should be a slice of element 1
        assert data == [self.input_data[0], self.input_data[2]]

    def test_filtering_math(self):
        from pyfsdb.tools.pdbrow import process_pdbrow

        input_data_fsdb = self.get_standard_input()
        output_data = StringIO()
        output_data.close = noop

        process_pdbrow(input_data_fsdb, output_data, "c == a*a*a")
    
        data = pyfsdb.Fsdb(file_handle=StringIO(output_data.getvalue()),
                           return_type=pyfsdb.RETURN_AS_DICTIONARY).get_all()

        # result should be a slice of element 1
        assert data == self.input_data[1:2]

    def test_filtering_(self):
        from pyfsdb.tools.pdbrow import process_pdbrow

        input_data_fsdb = self.get_standard_input()
        output_data = StringIO()
        output_data.close = noop

        process_pdbrow(input_data_fsdb, output_data, "c == a*a*a")
    
        data = pyfsdb.Fsdb(file_handle=StringIO(output_data.getvalue()),
                           return_type=pyfsdb.RETURN_AS_DICTIONARY).get_all()

        # result should be a slice of element 1
        assert data == self.input_data[1:2]
        
