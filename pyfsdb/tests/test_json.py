import unittest
from io import StringIO

class test_json_functions(unittest.TestCase):
    def test_json_to_fsdb(self):
        from pyfsdb.json2fsdb import json_to_fsdb
        self.assertTrue(json_to_fsdb, "loaded")

        inp = StringIO('{"d":"f", "a":"c"}' + "\n" + '{"a":"b", "d":"e"}')
        output = StringIO() # don't require converting to a string
        json_to_fsdb(inp, output)

        self.assertEqual(output.getvalue(),
                         "#fsdb -F t a d\nc\tf\nb\te\n",
                         "output of json_to_fsdb is correct")
        
