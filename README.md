# Objective

A python implementation of the [FSDB] flat-file streaming database.

[FSDB]: https://www.isi.edu/~johnh/SOFTWARE/FSDB/

# Installation

Using pip:

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

Read below for further usage details.

# Installation

```
pip3 install pyfsdb
```

# Additional Usage Details

The real power of the FSDB comes from the build up of tool-suites that
all interchange FSDB formatted files.  This allows chaining multiple
commands together to achieve a goal.  Though the original base set of
tools are in perl, you don't need to know perl for most of them.

## Let's create a ./mydemo command:

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
#   | ./test.py
```

Or chain it together with multiple FSDB commands:

```
# cat test.fsdb | ./mydemo | dbcolstats valueq
cat test.fsdb | PYTHONPATH=pyfsdb python3 ./test.py | dbcolstats value | dbcol mean stddev sum min max | dbfilealter -R C
#fsdb -R C mean stddev sum min max
mean: 165
stddev: 114.55
sum: 330
min: 84
max: 246

#   | ./test.py
#   | dbcolstats value
#   | dbcol mean stddev sum min max
#   | dbfilealter -R C
```

# See also

The FSDB website and manual page for the original perl module: 

https://www.isi.edu/~johnh/SOFTWARE/FSDB/
