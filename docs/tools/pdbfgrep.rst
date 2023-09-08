pdbfgrep - join rows from one FSDB files into another
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbfgrep`` provides a mechanism for doing a multi-match grep from
two FSDB files, where the first is the stream to read and grep from
(search through) and the second is a file containing a list of values
from keys to match against.  Similar to ``pdbaugment``, ``pdbfgrep``
is designed to read a single file entirely into memory and use it
search for rows in a second one that is read in a streaming style. In
general, the smaller file should be used as the *augment_file*
argument, and the larger as the ``stream_file`` when
possible.

Example input file 1 (*mygreptest.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F t col1 two andthree
   1   key1    42.0
   2   key2    123.0
   3   key3    90.2

Example input file 2 (*grep-values.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F t two additional_column
   key1    blue
   key3    brown

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbfgrep -k two -- mygreptest.fsdb grep-values.fsdb

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t col1:a two:a andthree:a
   1	key1	42.0
   3	key3	90.2
   #   | pdbfgrep --k two -- mygreptest.fsdb grep-values.fsdb

Example command usage -- inverted grep
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbfgrep -v -k two -- mygreptest.fsdb grep-values.fsdb

Example output
^^^^^^^^^^^^^^

::

    #fsdb -F t col1:a two:a andthree:a
    2	key2	123.0
    #   | pdbfgrep -v -k two -- mygreptest.fsdb grep-values.fsdb


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbfgrep
   :func: parse_args
   :hook:
   :prog: pdbfgrep
