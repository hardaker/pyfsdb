from pyfsdb.tools.pdbaugment import stash_row, find_row


def test_cache_saving():
    rows = [
        {"a": 1, "b": 2, "c": 3},
        {"a": 4, "b": 5, "c": 6},
    ]

    cache = {}

    for row in rows:
        stash_row(cache, ["a", "b"], row)

    open("/tmp/x", "w").write(str(cache) + "\n")

    assert cache == {
        1: {2: {"data": {"a": 1, "b": 2, "c": 3}}},
        4: {5: {"data": {"a": 4, "b": 5, "c": 6}}},
    }

    # now try looking up the results

    search_row = {"a": 1, "b": 2, "d": 33}
    result = find_row(cache, ["a", "b"], search_row)

    assert result == {"a": 1, "b": 2, "c": 3}

    result = find_row(cache, ["a", "b"], search_row, return_data=False)
    assert result == {"data": {"a": 1, "b": 2, "c": 3}}
