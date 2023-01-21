### pdbjinja - process an FSDB file with a jinja template

`pdbjinja` takes all the data in an fsdb file, and passes it to a
jinja2 template with each row being stored in a `rows` variable.

*Note:* all rows will be loaded into memory at once.

*See also:* `pdbformat`

#### Example input (*myfile.fsdb*):

```
#fsdb -F t col1:l two:a andthree:d
1	key1	42.0
2	key2	123.0
3	key1	90.2
```

#### Example jinja template (*myfile.j2*)

```
{% for row in rows -%}
Key {{row["two"]}}'s favorite number is {{row["andthree"]}}
{% endfor %}
```

#### Example command usage

```
$ pdbjinja -j myfile.j2 myfile.fsdb
```

#### Example output

```
Key key1's favorite number is 42.0
Key key2's favorite number is 123.0
Key key1's favorite number is 90.2
```


