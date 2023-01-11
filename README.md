# Objective

The [FSDB] "flat-file streaming database" is a structured data file
that includes column names, formatting specifications (e.g. tab vs
space vs comma), and a command history that generated each file.
PyFSDB is a a python implementation of the original functionality that
was implemented in perl.  Both the perl and python version come with a
long list of [command line tools] that can be used to quickly process
datasets using traditional unix pipeline processing.  There is also a
[C implementation] and a Go implementation (ref needed) of FSDB.

Getting started documentation is below, but also see the [full
documentation] over on readthedocs.

[FSDB]: https://www.isi.edu/~johnh/SOFTWARE/FSDB/
[C implementation]: https://github.com/hardaker/fsdb-clib
[full documentation]: https://fsdb.readthedocs.io/en/latest/
[command line tools]: https://fsdb.readthedocs.io/en/latest/tools/index.html

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
# cat test.fsdb | ./mydemo.py
#fsdb -F t col1 value
1	84.0
2	246.0
#   | ./mydemo.py
```

Or chain it together with multiple FSDB commands:

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

# Command line tools included

All the command line utilities that come with `pyfsdb` start with `p`
by convention so as not to conflict with the utilities from perl
package.  The leading `p` also serves to distinguish the CLI argument
differences as well (e.g. the python versions allow file names to be
specified on the command line, and most keys must be passed with a
`-k` flag).

## Data processing tools

- pdbrow: select rows based on logic criteria
- pdbroweval: modify rows based on python code
- pdbtopn: given a key and a value column, print the top N rows with
  unique keys and the highest values.
- pdbaugment: a fast way to merge two fsdb files, where one is stored
  entirely in memory for speed.  Unlike other tools, this does not
  sort the data for speed purposes.
- pdbcoluniq: find all unique values of a key column, optionally with
  counting.  Requires no sorting (unlike dbrowuniq) at the cost of
  greater memory usage.
- pdbzerofill: fills a column with zeros if the value is otherwise blank
- pdbkeyedsort: sorts a potentially large file that is already
  "mostly" sorted by performing a double-pass on reading it.  This
  will be less and less efficient the more random the rows are in
  order.
- pdbfullpivot: description TBD
- pdbreescape: converts a column full of data to regex quoted for
  safety
- pdbensure:
- pdbcdf: performs cdf analysis on a column

## Conversion tools
- bro2fsdb: converts a [zeek/bro](zeek.org) log into an fsdb
- json2fsdb: converts a json file to fsdb
- fsdb2json: converts an fsdb file to json
- pdb2tex: converts a fsdb file to a latex table
- pdbformat: generically formats each row according to a python column
  specifier
- pdbsplitter: splits a FSDB file into multiple sub-files based on a
  column set
- pdbdatetoepoch: converts columns from a date string to an integer
  epoch column
- pdbepochtodate: formats a unix epoch seconds date to human readable
- pdbnormalize: normalizes a column to a limited range
- pdbsum: tbd
- pdbj2: formats results based on a jinja2 template
- pdb2sql: converts a fsdb file into an sqlite3 database

## graphical utilities
- pdbheatmap: creates a heat map based on incoming data columns
- pdbroc: creates a ROC graph for incoming fsdb data


# Author

Wes Hardaker @ USC/ISI

# See also

The FSDB website and manual page for the original perl module:

https://www.isi.edu/~johnh/SOFTWARE/FSDB/
