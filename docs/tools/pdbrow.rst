pdbrow - select a subset of rows based on a filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbrow`` can apply an arbitrary logical python expression that selects
matching rows for passing to the output.

Example input (*myfile.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F s col1:l two:a andthree:d
   1   key1    42.0
   2   key2    123.0
   3   key1    90.2

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbrow 'col1 == "key1"' myfile.fsdb

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two andthree:d
   1   key1    42.0
   3   key1    90.2
   #   | pdbrow 'two == "key1"' myfile.fsdb

Example command usage with initialization code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbrow -i "import re" 're.match("key1", two)' myfile.fsdb

.. _example-output-1:

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two andthree:d
   1   key1    42.0
   3   key1    90.2
   #   | pdbrow -i 'import re' 're.match("key1", two)' myfile.fsdb


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbrow
   :func: parse_args
   :hook:
   :prog: pdbrow
