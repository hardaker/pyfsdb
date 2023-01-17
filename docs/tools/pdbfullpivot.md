### pdbfullpivot - translate a date-string based column to unix epochs

`pdbfullpivot` takes an input file with time/key/value pairs, and
pivots the table into a wide table with one new column per key value.

*TODO: make this more generic to allow N number of keying columns*

#### Example input (*myfile.fsdb*):

```
#fsdb -F t col1:l two:a andthree:d
1	key1	42.0
1	key2	123.0
2	key1    90.2
```

#### Example command usage

```
$ pdbfullpivot -t col1 -k two myfile.fsdb
```

#### Example output

```
#fsdb -F t col1:l key1:d key2:d
1	42.0	123.0
2	90.2	0
...
```

#### Notes

This can produce an output table with a lot of columns when there are
a lot of values within the key column.
