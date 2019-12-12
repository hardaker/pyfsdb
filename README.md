# Objective

A python implementation of the [FSDB] flat-file streaming database.

[FSDB]: https://www.isi.edu/~johnh/SOFTWARE/FSDB/

# Example Usage

The FSDB file format contains headers and footers that supplement the
data within a file.  The most common separator is tab-separated, but
can wrap CSVs and other datatypes (see the FSDB documentation for full
details).  The file also contains footers that trace all the piped
commands that were used to create a file, thus documenting the history
of its creation within the metadata in the file.

## Example pyfsdb code for reading a file

Reading in row by row:

```
import pyfsdb
db = pyfsdb.Fsdb("myfile.fsdb")
print(db.column_names)
for row in db:
    print(row)
```

## Example FSDB file

```
#fsdb -F t col1 two andthree
1	key1	42.0
2	key2	123.0
```

## Example writing to an FSDB formatted file.

```
import pyfsdb
db = pyfsdb.Fsdb(out_file="myfile.fsdb")
db.out_column_names=('one', 'two')
db.append([4, 'hello world'])
db.close()
```

# See also

The FSDB website and manual page for the original perl module: 

https://www.isi.edu/~johnh/SOFTWARE/FSDB/
