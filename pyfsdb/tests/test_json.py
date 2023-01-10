import unittest
from io import StringIO


class test_json_functions(unittest.TestCase):
    def test_json_to_fsdb(self):
        from pyfsdb.tools.json2fsdb import json_to_fsdb

        self.assertTrue(json_to_fsdb, "loaded")

        inp = StringIO(
            '{"d":"f", "a":"c"}'
            + "\n"
            + '{"a":"b", "d":"e"}'
            + "\n"
            + '{"d": "x", "c": "2", "a": "y"}'
            + "\n"
            '{"d": "x"}' + "\n"
        )
        output = StringIO()  # don't require converting to a string
        json_to_fsdb(inp, output)

        self.assertEqual(
            output.getvalue(),
            "#fsdb -F t a:a d:a\nc\tf\nb\te\ny\tx\n\tx\n",
            "output of json_to_fsdb is correct",
        )

    def test_fsdb_to_json(self):
        from pyfsdb.tools.fsdb2json import fsdb_to_json

        self.assertTrue(fsdb_to_json, "loaded")

        inp = StringIO("#fsdb -F t a d\nc\tf\nb\te\n")
        output = StringIO()

        fsdb_to_json(inp, output)

        self.assertEqual(
            output.getvalue(),
            '{"a": "c", "d": "f"}' + "\n" + '{"a": "b", "d": "e"}' + "\n",
            "output of fsdb_to_json is correct",
        )
