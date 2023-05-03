pdbzerofill - fills a columns with zeros (or other value) when blank
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbzerofill`` fills a row that is missing in a series of rows with a
numerical increasing (frequently a timestamp) index This is a sister
program to ``pdbensure`` which removes rows with missing data instead of
creating them.

Example input (*myblanks.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two:a andthree:d
   2   key1    42.0
   6   key2    
   10      90.2

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbzerofill -c two andthree -v xxx -b 2 -t col1

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two andthree:d
   2   key1    42.0
   4   xxx xxx
   6   key2    
   8   xxx xxx
   10      90.2


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbzerofill
   :func: parse_args
   :hook:
   :prog: pdbzerofill
