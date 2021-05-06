import unittest
import io

class test_pcdf(unittest.TestCase):
    def test_pcdf(self):
        from pyfsdb.tools.pdbcdf import process_cdf
        self.assertTrue(True, 'loaded module')

        in_data = io.StringIO("#fsdb -F t a b\n1\t2\n3\t6\n")
        out_data = io.StringIO()

        process_cdf(in_data, out_data, 'b')

        result = out_data.getvalue()

        self.assertEqual(result, "#fsdb -F t a b b_cdf\n1\t2\t0.25\n3\t6\t0.75\n",
                         "results (sum) were as expected")


        # use max() instead for the bottom
        in_data = io.StringIO("#fsdb -F t a b\n1\t2\n3\t4\n")
        out_data = io.StringIO()

        process_cdf(in_data, out_data, 'b', use_max=True)

        result = out_data.getvalue()

        self.assertEqual(result, "#fsdb -F t a b b_cdf\n1\t2\t0.5\n3\t4\t1.0\n",
                         "results (max) were as expected")
        
