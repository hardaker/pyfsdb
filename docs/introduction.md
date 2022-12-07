# Introduction

PyFSDB is a python implementation of the (perl) [FSDB] flat-file
streaming database.  See also, so my [C implementation] (under
development).

[FSDB]: https://www.isi.edu/~johnh/SOFTWARE/FSDB/
[C implementation]: https://github.com/hardaker/fsdb-clib

# Installation

Using pip (or pipx):

```
pip3 install pyfsdb
```

Or manually:

```
git clone git@github.com:gawseed/pyfsdb.git
cd pyfsdb
python3 setup.py build
python3 setup.py install
```

# Example Usage

The FSDB file format contains headers and footers that supplement the
data within a file.  The most common separator is tab-separated, but
can wrap CSVs and other datatypes (see the FSDB documentation for full
details).  The file also contains footers that trace all the piped
commands that were used to create a file, thus documenting the history
of its creation within the metadata in the file.

## Example FSDB file

The following is an example FSDB formatted file, that is tab separated
(`-F t`) with three columns (`col1` - a long/integer, `two` - a
string, and `three` - a double/float).

```
#fsdb -F t col1:l two:s andthree:d
1	key1	42.0
2	key2	123.0
```

## Example code for reading a FSDB file

The following code reads the above file (stored in `myfsdb.fsdb`), and
prints the column names automatically seen, the converters that come
from the type specifiers (`:l`, `:a`, and `:d`) and each row (in array format).

### Code:

``` python
import pyfsdb
db = pyfsdb.Fsdb("myfile.fsdb")
print(db.column_names)
print(db.converters)
for row in db:
    print(row)
```

### Output:

```
['col1', 'two', 'andthree']
{'col1': <class 'int'>, 'andthree': <class 'float'>}
[1, 'key1', 42.0]
[2, 'key2', 123.0]
```

## Example writing an FSDB formatted file.

```
import pyfsdb
db = pyfsdb.Fsdb(out_file="myfile.fsdb")
db.out_column_names=('one', 'two')
db.append([4, 'hello world'])
db.close()
```

Read below for further usage details.

