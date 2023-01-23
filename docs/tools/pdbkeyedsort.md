### pdbkeyedsort - find all unique values of a key column

Sort "mostly sorted" large FSDB files using a double pass dbkeyedsort
reads a file twice, sorting the data by the column specified via the
-c/--column option.  During the first pass, it counts all the rows per
key to manage which lines it needs to memorize as it is making its
second pass. During the second pass, it only stores in memory the
lines that are out of order. This can greatly optimize the amount of
memory stored when the data is already in a fairly sorted state (which
is common for the output of map/reduce operations such as
hadoop). This comes at the expense of needing to read the entire
dataset twice, which means its impossible to use `stdin` to pass in
data; instead a filename must be specified instead.  The output,
though, may be `stdout`.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

We add the -v flag to have it give a count of the number of lines that
were cached.  In general, you want this fraction to be small to
conserve memory.  In the example below, `pdbkeyedsort` only needed to
memorize one row (the second) of the above file.

```
$ pdbkeyedsort -c andthree -v  myfile.fsdb
```

#### Example output

```
#fsdb -F t col1:l two andthree:d
1	key1	42.0
3	key1	90.2
2	key2	123.0
cached 1/3 lines
```
