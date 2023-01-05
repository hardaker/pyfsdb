### pdb2to1 - strip typing information from the FSDB header

`pdb2to1` simply removes typing information that may confusing older
FSDB or pyfsdb tools that do not understanding datatypes in the
headers.  Datatypes were introduced into FSDB format version 2.  To
add or change types instead, use `pdbaddtypes`.

#### Example input (*myfile.fsdb*):

```
#fsdb -F t col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1	90.2
```

#### Example command usage

```
$ pdb2to1 myfile.fsdb
```

#### Example output

```
#fsdb -F t col1 two andthree
1	key1	42.0
2	key2	123.0
3	key1	90.2
```

