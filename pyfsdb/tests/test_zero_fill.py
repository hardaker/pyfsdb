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
