### pdbtopn - selects the top N rows based on values from a column

`pdbtopn` selects N rows from an FSDB file by selecting the top values
from a particular column.  For smaller datasets, using a combination
of `dbsort` and `dbuniq` accomplish the same functional result.
However, `pdbtopn` requires far less memory and CPU computation when N
is small and the dataset is large.  Using `dbsort` and `dbuniq` may be
a better solution with very large values of N.

#### Example input (*myfile.fsdb*):

```
#fsdb -F s col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1    90.2
```

#### Example command usage

```
$ pdbtopn -k two -n 1 -v andthree myfile.fsdb
```

#### Example output

```
#fsdb -F t col1:l two andthree:d
2	key2	123.0
```

#### Example selecting the top values of multiple keys

```
$ pdbtopn -k two -n 20 -v andthree myfile.fsdb
```
#### Example output


```
#fsdb -F t col1:l two andthree:d
3	key1	90.2
2	key2	123.0
```
