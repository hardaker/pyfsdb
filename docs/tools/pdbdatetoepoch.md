### pdbdatetoepoch - translate a date-string based column to unix epochs

`pdbdatetoepoch` translates one date/time based column column to
another unix epoch seconds (since Jan 1 1970) column.

#### Example input (*mytime.fsdb*):

```
#fsdb -F t index:d datecol:a
1	2023/01/01
2	2023/01/01 10:50:05
```

#### Example command usage

```
$ pdbdatetoepoch -d datecol -t timestamp percent mytime.fsdb
```

#### Example output

```
#fsdb -F t col1 two andthree andthree_cdf raw percent
1	key1	42.0	0.164576802507837	42.0	16.4576802507837
2	key2	123.0	0.646551724137931	165.0	48.19749216300941
3	key1	90.2	1.0	255.2	35.3448275862069
...
```

#### Notes

Internally this uses python's `dateparser` module.
