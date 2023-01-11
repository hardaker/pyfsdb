### pdbformat - create formatted text per row in an FSDB file

`pdbformat` uses python's internal string formatting mechanisms to
output lines of text based on the column values from each row.  The
*-f* flag is used to specify the formatting string to use, where
column names maybe enclosed in curly braces to indicate where
replacement should happen.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

```
$ pdbformat -f "{two} is {andthree:>7.7} !" myfile.fsdb
```

#### Example output

```
key1 is    42.0 !
key2 is   123.0 !
key1 is    90.2 !
```
