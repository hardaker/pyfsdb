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

### Code:

```
import pyfsdb
db = pyfsdb.Fsdb(out_file="myfile.fsdb")
db.out_column_names=('one', 'two')
db.append([4, 'hello world'])
db.close()
```

### Output:

```
#fsdb -F t one:l two
4	hello world
```

# A larger example

The real power of the FSDB comes from the build up of tool-suites that
all interchange FSDB formatted files.  This allows chaining multiple
commands together to achieve a goal.  Though the original base set of
tools are in perl, you don't need to know perl for most of them.

## Let's create a ./mydemo.py script:

``` python
import sys, pyfsdb

db = pyfsdb.Fsdb(file_handle=sys.stdin, out_file_handle=sys.stdout)
value_column = db.get_column_number('value')

for row in db:     # reads a row from the input stream
    row[value_column] = float(row[value_column]) * 2
    db.append(row) # sends the row to the output stream

db.close()
```

And then feed it this file:

```
#fsdb -F t col1 value
1	42.0
2	123.0
```

We can run it thus'ly:


``` sh
# cat test.fsdb | ./mydemo
#fsdb -F t col1 value
1	84.0
2	246.0
#   | ./mydemo.py
```

Or chain it together with multiple FSDB commands.  Note the details of
the chain are recorded at the bottom of the output file.

```
# cat test.fsdb | ./mydemo | dbcolstats value | dbcol mean stddev sum min max | dbfilealter -R C
#fsdb -R C mean stddev sum min max
mean: 165
stddev: 114.55
sum: 330
min: 84
max: 246
#   | ./mydemo.py
#   | dbcolstats value
#   | dbcol mean stddev sum min max
#   | dbfilealter -R C
```
