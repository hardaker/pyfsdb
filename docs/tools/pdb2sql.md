### pdb2sql - uploads an FSDB file into a database

`pdb2sql` converts an FSDB file into a latex table/tabular output.  Specifically, it can both create a table, delete existing rows, add indexes to certain rows, add additional columns and values etc.  It currently supports two different types of databases (*sqlite3* and *postgres*), which are selectable by the *-t* switch.

#### Example input (*myfile.fsdb*):

```
#fsdb -F t col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1	90.2
```

#### Example command usage

```
$ pdb2sql -T newtable -i two -t sqlite3 myfile.fsdb output.sqlite3
$ echo "select * from newtable" | sqlite3 output.sqlite3 
```

#### Example output

```
1|key1|42.0
2|key2|123.0
3|key1|90.2
```

