from io import StringIO
import pyfsdb
from pyfsdb.tools.pdbzerofill import fill_values


def test_fillempty_single_column():
    """Tests that proper bin-filling happens with empty columns"""
    indata = StringIO("#fsdb -F s a:a b:l\n60 1\n120 2\n240 4\n480 8")
    outdata = StringIO()

    def noop():
        pass

    results = None
    with pyfsdb.Fsdb(
        file_handle=indata,
        out_file_handle=outdata,
        out_column_names=["no", "third"],
    ) as fh:
        outdata.close = noop
        fill_values(fh, key_column="a", columns="b", value=42, bin_size=60)
        results = outdata.getvalue()

    with pyfsdb.Fsdb(file_handle=StringIO(results)) as fh:
        data = fh.get_all()
        assert data == [
            ["60", 1],
            ["120", 2],
            ["180", 42],
            ["240", 4],
            ["300", 42],
            ["360", 42],
            ["420", 42],
            ["480", 8],
        ]


def test_fillempty_copy_other_keys():
    """Check that multiple key filling is supported (copied from previous)"""
    indata = StringIO("#fsdb -F s a:a b:l c:a\n60 1 aa\n120 2 bb\n240 4 cc\n480 8 dd")
    outdata = StringIO()

    def noop():
        pass

    results = None
    with pyfsdb.Fsdb(
        file_handle=indata,
        out_file_handle=outdata,
        out_column_names=["no", "third"],
    ) as fh:
        outdata.close = noop
        fill_values(
            fh, key_column="a", columns="b", value=42, bin_size=60, other_keys="c"
        )
        results = outdata.getvalue()

    with pyfsdb.Fsdb(file_handle=StringIO(results)) as fh:
        data = fh.get_all()
        assert data == [
            ["60", 1, "aa"],
            ["120", 2, "bb"],
            ["180", 42, "bb"],
            ["240", 4, "cc"],
            ["300", 42, "cc"],
            ["360", 42, "cc"],
            ["420", 42, "cc"],
            ["480", 8, "dd"],
        ]
