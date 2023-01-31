### pdbsplitter - split an FSDB file into multiple files

`pdbsplitter` splits a single FSDB file into a series of output files.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

```
$ pdbsplitter -k col1 -c two andthree -o myfile-split-%s.fsdb myfile.fsdb
```

#### Example output

The above command produces two different files, one per each column.

- *myfile-split-two.fsdb*:

```
#fsdb -F t col1 two
1	key1
2	key2
3	key1
```

- *myfile-split-andthree.fsdb*:

```
#fsdb -F t col1 andthree
1	42.0
2	123.0
3	90.2
```
