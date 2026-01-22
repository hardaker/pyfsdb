from io import StringIO
import pyfsdb
from pyfsdb.tools.pdbzerofill import fill_values
from pyfsdb.tests.support import encode_to_fsdb, extract_fsdb_data

try:
    from rich import print
except Exception:
    pass


def noop():
    pass


def perform_fill_test_with_data(starting_data: list, *args, **kwargs):
    """converts the start_data to fsdb, then calls fill data and
    returns the decode results."""
    indata = StringIO(encode_to_fsdb(starting_data))
    outdata = StringIO()
    outdata.close = noop

    filled_data = None

    with pyfsdb.Fsdb(
        file_handle=indata,
        out_file_handle=outdata,
    ) as fh:
        fill_values(fh, *args, **kwargs)

        filled_data = extract_fsdb_data(outdata.getvalue())

    return filled_data


def test_fillempty_single_column():
    """Tests that proper bin-filling happens with empty columns"""
    indata = StringIO("#fsdb -F s a:a b:l\n60 1\n120 2\n240 4\n480 8")
    outdata = StringIO()

    results = None
    with pyfsdb.Fsdb(
        file_handle=indata,
        out_file_handle=outdata,
    ) as fh:
        outdata.close = noop
        fill_values(fh, key_column="a", columns=["b"], value=42, bin_size=60)
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


def test_fillempty_multiple_columns():
    """Tests that proper bin-filling happens with multiple columns"""
    indata = StringIO("#fsdb -F s a:a b:l c:l\n60 1 11\n120 2 22\n240 4 44\n480 8 88")
    outdata = StringIO()

    def noop():
        pass

    results = None
    with pyfsdb.Fsdb(
        file_handle=indata,
        out_file_handle=outdata,
    ) as fh:
        outdata.close = noop
        fill_values(fh, key_column="a", columns=["b", "c"], value=42, bin_size=60)
        results = outdata.getvalue()

    with pyfsdb.Fsdb(file_handle=StringIO(results)) as fh:
        data = fh.get_all()
        assert data == [
            ["60", 1, 11],
            ["120", 2, 22],
            ["180", 42, 42],
            ["240", 4, 44],
            ["300", 42, 42],
            ["360", 42, 42],
            ["420", 42, 42],
            ["480", 8, 88],
        ]


def test_fillempty_copy_other_keys():
    """Check that multiple other columns copying is supported (copied from previous)."""
    indata = StringIO("#fsdb -F s a:a b:l c:a\n60 1 aa\n120 2 bb\n240 4 cc\n480 8 dd")
    outdata = StringIO()

    def noop():
        pass

    results = None
    with pyfsdb.Fsdb(
        file_handle=indata,
        out_file_handle=outdata,
    ) as fh:
        outdata.close = noop
        fill_values(fh, key_column="a", columns=["b"], value=42, bin_size=60)
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


def test_fillempty_ignore_initial_missing():
    """Tests that we ignore keys we haven't seen yet."""
    starting_data = [
        [-120, "foo", -120],
        # bar -120 doesn't exist, but we don't know that yet which is ok
        # thus it won't be filled
        [-60, "foo", -4],
        [-60, "bar", -3],
    ]
    filled_data = perform_fill_test_with_data(
        starting_data,
        key_column="a",
        columns=["c"],
        value=42,
        bin_size=60,
        other_keys=["b"],
    )
    assert filled_data == [
        [-120, "foo", -120],
        [-60, "foo", -4],
        [-60, "bar", -3],
    ]


def test_skipping_all_keys():
    """has multiple indexes and then skips them all to ensure they're filled."""
    starting_data = [
        [0, "bar", 0],
        [0, "foo", 1],
        [60, "bar", 2],
        [60, "foo", 3],
        # 120 is skipped
        [180, "bar", 20],
        [180, "foo", 30],
    ]
    filled_data = perform_fill_test_with_data(
        starting_data,
        key_column="a",
        columns=["c"],
        value=42,
        bin_size=60,
        other_keys=["b"],
    )
    assert filled_data == [
        [0, "bar", 0],
        [0, "foo", 1],
        [60, "bar", 2],
        [60, "foo", 3],
        # 120 is filled:
        [120, "foo", 42],  # sorting reorders for some reason
        [120, "bar", 42],
        [180, "bar", 20],
        [180, "foo", 30],
    ]


def test_copying_of_other_columns():
    """Test copying of previous rows from previous other keysets"""
    starting_data = [
        [0, "bar", 0, "a"],
        [0, "foo", 1, "b"],
        [60, "bar", 2, "c"],
        [60, "foo", 3, "d"],
        # 120 is skipped
        [180, "bar", 20, "e"],
        [180, "foo", 30, "f"],
    ]
    filled_data = perform_fill_test_with_data(
        starting_data,
        key_column="a",
        columns=["c"],
        value=42,
        bin_size=60,
        other_keys=["b"],
    )
    assert filled_data == [
        [0, "bar", 0, "a"],
        [0, "foo", 1, "b"],
        [60, "bar", 2, "c"],
        [60, "foo", 3, "d"],
        # 120 is filled:
        [120, "foo", 42, "d"],  # sorting reorders for some reason
        [120, "bar", 42, "c"],
        [180, "bar", 20, "e"],
        [180, "foo", 30, "f"],
    ]


def test_copying_of_other_columns():
    """Test partial filling."""
    starting_data = [
        [0, "bar", 0, "a"],
        [0, "foo", 1, "b"],
        [60, "bar", 2, "c"],
        # 60 is skipped for foo only
        [120, "bar", 20, "e"],
        [120, "foo", 30, "f"],
    ]
    filled_data = perform_fill_test_with_data(
        starting_data,
        key_column="a",
        columns=["c"],
        value=42,
        bin_size=60,
        other_keys=["b"],
    )
    assert filled_data == [
        [0, "bar", 0, "a"],
        [0, "foo", 1, "b"],
        [60, "bar", 2, "c"],
        # 60/foo is filled with the last row's d and 42 in c:
        [60, "foo", 42, "b"],
        [120, "bar", 20, "e"],
        [120, "foo", 30, "f"],
    ]


def test_copying_of_alternating_columns():
    """Test partial filling with alternating missing keys."""
    starting_data = [
        [0, "bar", 0, "a"],
        [0, "foo", 1, "b"],
        [60, "bar", 2, "c"],
        # 60 is skipped for foo
        [120, "foo", 4, "bb"],
        # 120 is skipped for bar
        [180, "bar", 20, "e"],
        [180, "foo", 30, "f"],
    ]
    filled_data = perform_fill_test_with_data(
        starting_data,
        key_column="a",
        columns=["c"],
        value=42,
        bin_size=60,
        other_keys=["b"],
    )
    assert filled_data == [
        [0, "bar", 0, "a"],
        [0, "foo", 1, "b"],
        [60, "bar", 2, "c"],
        [60, "foo", 42, "b"],
        [120, "foo", 4, "bb"],
        [120, "bar", 42, "c"],
        [180, "bar", 20, "e"],
        [180, "foo", 30, "f"],
    ]


def test_fillempty_with_only_some_keys():
    """This tests multiple cases of missing other_keys column data.

    Note: it also checks that negative values in time work."""
    starting_data = [
        [-120, "foo", -120],
        [-60, "foo", -4],
        [-60, "bar", -3],
        # foo 0 is missing
        [0, "bar", -1],
        [60, "foo", 1],
        [60, "bar", 2],
        [120, "foo", 3],
        # bar 120 missing
        [180, "bar", 4],
        # foo 180 missing
        [240, "foo", 5],
        [240, "bar", 5],
        # foo/bar 300 and beyond all missing, but bar returns at 480
        [480, "bar", 60],
    ]
    filled_data = perform_fill_test_with_data(
        starting_data,
        key_column="a",
        columns=["c"],
        value=42,
        bin_size=60,
        other_keys=["b"],
    )
    print(filled_data)
    assert filled_data == [
        [-120, "foo", -120],
        [-60, "foo", -4],
        [-60, "bar", -3],
        [0, "bar", -1],
        [0, "foo", 42],
        [60, "foo", 1],
        [60, "bar", 2],
        [120, "foo", 3],
        [120, "bar", 42],
        [180, "bar", 4],
        [180, "foo", 42],
        [240, "foo", 5],
        [240, "bar", 5],
        [300, "bar", 42],
        [300, "foo", 42],
        [360, "bar", 42],
        [360, "foo", 42],
        [420, "bar", 42],
        [420, "foo", 42],
        [480, "bar", 60],
        [480, "foo", 42],
    ]
