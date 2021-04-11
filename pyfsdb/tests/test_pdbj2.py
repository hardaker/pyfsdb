#!/usr/bin/python3

from unittest import TestCase
import pyfsdb
from io import StringIO

def noop(**kwargs):
    pass

class pdbj2Test(TestCase):
    def test_loading_pdbj2(self):
        import pyfsdb.tools.pdbj2
        self.assertTrue("loaded")

    def test_pdbj2(self):
        input_data = "#fsdb -F t a b c\n1\t2\t3\nd\te\tf\n"
        inputh = StringIO(input_data)

        j2_template = "{% for row in rows %}{{row.b}}\n{% endfor %}"
        j2h = StringIO(j2_template)

        outh = StringIO()
        outh.close = noop

        import pyfsdb.tools.pdbj2
        pyfsdb.tools.pdbj2.process(inputh, j2h, outh)
        self.assertTrue("ran")

        # actually test the results
        result = outh.getvalue()
        self.assertEqual(result, "2\ne\n",
                         "expected template results are correct")
