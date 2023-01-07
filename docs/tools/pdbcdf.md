### pdbcdf - find all unique values of a key column

`pdbcdf` analyzes one column from an FSDB file to produce normalized
CDF related columns.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

```
$ pdbcoluniq -c andthree -P percent -R raw myfile.fsdb
```

#### Example output

```
#fsdb -F t col1 two andthree andthree_cdf raw percent
1	key1	42.0	0.164576802507837	42.0	16.4576802507837
2	key2	123.0	0.646551724137931	165.0	48.19749216300941
3	key1	90.2	1.0	255.2	35.3448275862069
...
```
