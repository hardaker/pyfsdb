### pdbcoluniq - find all unique values of a key column

`pdbcoluniq` can find all unique values of a key column, optionally
including counting the number of each value seen.  This is done with
an internal dictionary and requires no sorting (unlike its perl
dbrowuniq equivelent) at the potential cost of higher memory usage.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

```
$ pdbcoluniq -k two -c myfile.fsdb
```

#### Example output

```
#fsdb -F t two count:l
key1	2
key2	1
#   | pdbcoluniq -k two -c myfile.fsdb
```
