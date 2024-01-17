from unittest import TestCase
import pyfsdb
import io
import re


def truncate_comments(value):
    value = re.sub("\n# +\\|.*", "", value)
    return value


class FsdbMsgPackTest(TestCase):
    fsdb_data = "#fsdb -F s a:l b:l\n1 2\n"
    encoded_data = b"#fsdb -F m a:l b:l\n\x92\x01\x02"

    def test_convert_to_msgpack(self):
        ih = pyfsdb.Fsdb(file_handle=io.StringIO(self.fsdb_data))

        def noop(*args, **kwargs):
            pass

        out_data = io.BytesIO()
        out_data.close = noop

        oh = pyfsdb.Fsdb(out_file_handle=out_data)
        oh.out_column_names = ih.column_names
        oh.converters = ih.converters
        oh.out_separator = "m"

        for row in ih:
            oh.append(row)
        oh.close()

        # the output data we expect should be:
        self.assertEqual(out_data.getvalue(), self.encoded_data)

    def test_convert_from_msgpack(self):
        ih = pyfsdb.Fsdb(file_handle=io.BytesIO(self.encoded_data))

        def noop(*args, **kwargs):
            pass

        out_data = io.StringIO()
        out_data.close = noop

        oh = pyfsdb.Fsdb(out_file_handle=out_data)
        oh.out_column_names = ih.column_names
        oh.converters = ih.converters
        oh.out_separator = " "

        for row in ih:
            oh.append(row)
        oh.close()

        # the output data we expect should be:
        results = out_data.getvalue()
        self.assertEqual(truncate_comments(results), self.fsdb_data)
