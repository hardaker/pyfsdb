### pdbsankey - Produce a sankey diagram from FSDB column data

`pdbsankey` produces a
[SANKEY](https://en.wikipedia.org/wiki/Sankey_diagram) diagram given
values in an FSDB file.  A source, destination and count column are
expected in the data in order to plot the results.

#### Example input (*mysankey.fsdb*):

Consider the following example input file, where A1 and A2 lead to B1,
and B2 and then further to C1 and C2:

```
#fsdb -F s source destination count
A1 B1 8
A2 B2 4
A1 B2 2
B1 C1 8
B2 C1 4
B2 C2 2
```

#### Example command usage

We can then run `pdbsankey` to generate a diagram based on these values.

```
$ pdbheatmap --title "Example Sankey" mysankey.fsdb mysankey.png
```

#### Example output

![mysankey.png](images/mysankey.png)
