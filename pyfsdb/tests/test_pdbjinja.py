from unittest import TestCase
import pyfsdb
from io import StringIO


def noop(**kwargs):
    pass


class pdbjinjaTest(TestCase):
    def test_loading_pdbjinja(self):
        import pyfsdb.tools.pdbjinja

        self.assertTrue("loaded")

    def test_pdbjinja(self):
        input_data = "#fsdb -F t a b c\n1\t2\t3\nd\te\tf\n"
        inputh = StringIO(input_data)

        jinja_template = "{% for row in rows %}{{row.b}}\n{% endfor %}"
        jinjah = StringIO(jinja_template)

        outh = StringIO()
        outh.close = noop

        import pyfsdb.tools.pdbjinja

        pyfsdb.tools.pdbjinja.process(inputh, jinjah, outh)
        self.assertTrue("ran")

        # actually test the results
        result = outh.getvalue()
        self.assertEqual(result, "2\ne\n", "expected template results are correct")
