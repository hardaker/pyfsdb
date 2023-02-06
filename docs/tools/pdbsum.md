### pdbsum - sum columns together

`pdbsum` adds column data together based on keyed input.  This is
similar to `dbcolstats` and `dbmultistats`, but only performs addition
(or subtraction) and can be faster on very large datasets where the
rest of the analysis provided by the other tools are not needed.
`dbsum` also supports keyed subtraction as well, as seen below.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

```
$ pdbsum -k two -c col1 andthree -- myfile.fsdb
```

#### Example output

```
#fsdb -F t two col1:d andthree:d
key1	4.0	132.2
key2	2.0	123.0
```

#### Example Subtraction file

If we have another file (*mysub.fsdb*), we can subtract results:

```
#fsdb -F s two:a andthree:d
key1	10
key2	10
key1    10
```

#### Example subtraction command:

```
pdbsum -k two -c col1 andthree -- myfile.fsdb mysub.fsdb
```

#### Example output of subtraction:

Note how the two 10's in the key1 subtraction are added together to 20
before being subtracted from the sum of key1 (123.2) in the first
file.

*Note:* Also observe the typical floating point imprecision rounding
problems that python is well known for displaying.

```
#fsdb -F t two andthree:d
key1	112.19999999999999
key2	113.0
```
