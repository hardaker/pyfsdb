# Objective

A python implementation of the [FSDB] flat-file streaming database.

[FSDB]: https://www.isi.edu/~johnh/SOFTWARE/FSDB/

# Example Usage

```
import pyfsdb
db = pyfsdb.Fsdb("myfile.fsdb")
for row in db:
    print(row)
```

# See also

The FSDB website and manual page (perl)
