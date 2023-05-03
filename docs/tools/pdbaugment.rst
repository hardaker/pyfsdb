pdbaugment - join rows from one FSDB files into another
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbaugment`` provides a different mechanism for doing FSDB file joins
than the ``dbjoin`` command from the base perl FSDB package.
Specifically, ``pdbaugment`` is designed to read a single file entirely
into memory and use it augment a second one that is read in a streaming
style. ``pdbaugment`` has the advantage being faster because it dose not
need to do a full sort of both files, like ``dbjoin`` requires, but has
the downside of needing to store one file in memory while performing the
join. In general, the smaller file should be used as the *augment_file*
argument, and the larger as the ``stream_file`` when possible. Matching
keys in the augment file should be unique across the file, otherwise
only the second row with a give key combination will be used.

Example input file 1 (*myfile.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F t col1 two andthree
   1   key1    42.0
   2   key2    123.0
   3   key1    90.2

Example input file 2 (*augment.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F t col1 additional_column
   key1    blue
   key2    brown

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbaugment -k two -v additional_column -- myfile.fsdb augment.fsdb

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two:a andthree:d additional_column:a
   1   key1    42.0    blue
   2   key2    123.0   brown
   3   key1    90.2    blue


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbaugment
   :func: parse_args
   :hook:
   :prog: pdbaugment
