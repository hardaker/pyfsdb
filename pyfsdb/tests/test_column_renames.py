import unittest
from io import StringIO
import pyfsdb

class FsdbTestColumnRename(unittest.TestCase):
    def test_column_renames(self):
        input_data = "#fsdb -F s one two\n1 2\n"
        fh = StringIO(input_data)
        fs = pyfsdb.Fsdb(file_handle=fh,
                         return_type=pyfsdb.RETURN_AS_DICTIONARY)

        fs.column_names = ["_" + x for x in fs.column_names]

        data = next(fs)

        expected = { "_one": '1', "_two": '2' }

        self.assertEqual(data, expected,
                         "failed to remap columns on the fly")
        
