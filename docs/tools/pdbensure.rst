pdbensure - ensure certain columns are present in the data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbensure`` either simply drops rows without content in a list of
columns, or optionally fills in the values with a default instead.

Example input (*myfile.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F s col1:l two:a andthree:d
   1   key1    42.0
   2   key2    
   3       90.2

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbensure -c andthree -e myfile.fsdb

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two:a andthree:d
   1       42.0
   # dbensure dropping row:[2, 'key2', None]
   3       90.2

Example command usage – adding a second column
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbensure -c andthree two -e myfile.fsdb

.. _example-output-1:

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two:a andthree:d
   1       42.0
   # dbensure dropping row:[2, 'key2', None]
   # dbensure dropping row:[3, None, 90.2]

Example command usage – with replacement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbensure -c two -v replace -- myfile.fsdb

.. _example-output-2:

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two:a andthree:d
   1   key1    42.0
   2   key2    
   3   replace 90.2


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbensure
   :func: parse_args
   :hook:
   :prog: pdbensure
