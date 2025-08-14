### pdbpathtrack - track values of IDs as they shift from one category to another

`pdbpathtrack` provides a mechanism to for tracking generic entities
via their IDs as they traverse from one category to another.  This
tool is specifically designed to help generate Sankey diagrams, like
those produced in `pdfsankey`.

#### Example input file 1 (*myfile.fsdb*):

```
#fsdb -F s id category value
probe1 run1 foo
probe2 run1 foo
probe3 run1 bar
probe4 run1 foo
# ---
probe1 run2 bar
probe2 run2 bar
probe3 run2 bar
probe4 run2 foo
```

#### Example command usage

```
$ pdbpathtrack myfile.fsdb
#fsdb -F t source:a destination:a count:l
foo     bar     2
foo     foo     1
bar     bar     1
```

For multiple categories with similar values, you might want to prepend
the category label from a column too to make sure the path results are
distinguishable.  For example, in the above results a graph might be
drawn with a circular loop from foo back to foo with a value of 1.  To
fix this and make the labels unique, the category column can be to the
source/destination columns:

```
$ pdbpathtrack -c category myfile.fsdb
#fsdb -F t source:a destination:a count:l
run1:foo        run2:bar        2
run1:foo        run2:foo        1
run1:bar        run2:bar        1
```
