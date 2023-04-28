pdbreescape - regexp escape strings from a column
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbreescape`` passes the requested columns (-k) through python’s regex
escaping function.

\**Note: because -k can take multiple columns, input files likely need
to appear after the “–” argument-stop-parsing string.\*

Example input (*myfile.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F s col1:l two:a andthree:d
   1   key1    42.0
   2   key2    123.0
   3   key1    90.2

Example command usage
^^^^^^^^^^^^^^^^^^^^^

Using our standard input file for this documentation set, we first pass
the file through ``pdbaddtypes`` to change the type from a float to a
string, and then escape the period in the (now string) floating point
number:

::

   $ pdbaddtypes -t andthree=a -- myfile.fsdb |
     pdbreescape -k andthree

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two andthree
   1   key1    42\.0
   2   key2    123\.0
   3   key1    90\.2
   #   | /home/hardaker/.local/bin/pdbreescape -k andthree

A more complex file (*mystrings.fsdb*)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This shows a greater number of regex escaping types. Note that the
spaces are also escaped.

::

   #fsdb -F t type value
   wild-cards  * and . and + and ?
   parens  () and []
   slashes / and \

.. _example-command-usage-1:

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbreescape -k value -- mystrings.fsdb

.. _example-output-1:

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t type value
   wild-cards  \*\ and\ \.\ and\ \+\ and\ \?
   parens  \(\)\ and\ \[\]
   slashes /\ and\ \\


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbreescape
   :func: parse_args
   :hook:
   :prog: pdbreescape
