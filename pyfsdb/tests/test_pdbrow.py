from io import StringIO
import unittest
from logging import error

class test_pdbrow(unittest.TestCase):
    def test_load(self):
        from pyfsdb.tools.pdbrow import process_pdbrow
        self.assertTrue(True, "could load")

    def convert_to_stringio(self, data):
        import pyfsdb
        outh = StringIO()
        oh = pyfsdb.Fsdb(out_file_handle=outh)
        oh.out_column_names = list(data[0].keys())
        for row in data:
            oh.append(list(row.values()))
        return StringIO(outh.getvalue())

    def test_no_filtering(self):
        from pyfsdb.tools.pdbrow import process_pdbrow
        import pyfsdb
        input_data = [
            {'a': 5, 'b': 10, 'c': 15},
            {'a': 2, 'b': 4, 'c': 8},
            {'a': 3, 'b': 6, 'c': 12},            
        ]

        input_data_fsdb = self.convert_to_stringio(input_data)
        output_data = StringIO()
        process_pdbrow(input_data_fsdb, output_data, "True")
        
        data = pyfsdb.Fsdb(file_handle=StringIO(output_data.getvalue()),
                           return_type=pyfsdb.RETURN_AS_DICTIONARY).get_all()

        assert data == input_data
