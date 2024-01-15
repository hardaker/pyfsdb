from unittest import TestCase
import pyfsdb
import io


class FsdbMsgPackTest(TestCase):
    fsdb_data = "#fsdb -F s a:l b:l\n1 2"

    def test_convert_to_msgpack(self):
        ih = pyfsdb.Fsdb(file_handle=io.StringIO(self.fsdb_data))

        def noop(*args, **kwargs):
            pass

        out_data = io.BytesIO()
        out_data.close = noop

        oh = pyfsdb.Fsdb(out_file_handle=out_data)
        oh.out_column_names = ih.column_names
        oh.out_separator = "m"

        for row in ih:
            oh.append(row)
        oh.close()

        # the output data we expect should be:
        self.assertEqual(out_data.getvalue(), b"#fsdb -F m a b\n\x92\x01\x02")
