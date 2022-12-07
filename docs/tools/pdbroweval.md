### pdbroweval - alter rows based on python expressions or code

`pdbroweval` can apply an arbitrary python expression or code to
modify the contents of the file before passing it to the output
stream.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:s andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

```
$ pdbroweval 'andthree *= 2' myfile.fsdb
```

#### Example output

```
#fsdb -F t col1:l two andthree:d
1	key1	84.0
2	key2	246.0
3	key1	180.4
#   | pdbroweval 'andthree *= 2' myfile.fsdb
```

#### Example command usage with initialization code


```
$ pdbroweval -i "import re" 're.sub("key", "lock", two)' myfile.fsdb
```

#### Example output

```
#fsdb -F t col1:l two andthree:d
1	lock1	42.0
2	lock2	123.0
3	lock1	90.2
#   | pdbroweval -i import re two = re.sub("key", "lock", two) myfile.fsdb
```

#### Other options

- *-i*: indicates that the initialization code block specified by *-i*
  should be loaded from a file instead of a raw expression.

- *-f*: indicates that the initialization code block specified in
  *expression* should be loaded from a file instead of a raw
  expression.
