def test_label_shrink():
    from pyfsdb.tools.pdbheatmap import maybe_shrink_label

    assert True

    assert maybe_shrink_label("foo") == "foo"
    assert maybe_shrink_label("o" * 20) == "o" * 20
    assert maybe_shrink_label("o" * 10 + "p" * 10) == "o" * 10 + "p" * 10
    assert maybe_shrink_label("o" * 11 + "p" * 11, 20) == "o" * 9 + "..." + "p" * 8
    assert maybe_shrink_label("o" * 10 + "p" * 11, 20) == "o" * 9 + "..." + "p" * 8
    assert maybe_shrink_label("o" * 100 + "p" * 11000, 20) == "o" * 9 + "..." + "p" * 8
