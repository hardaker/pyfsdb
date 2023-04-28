pdbnormalize - normalize a bunch of columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbnormalize`` takes an input file and takes each column value from a
number of columns and divides it by the maximum value seen in all the
columns.

*Note: this is the maximum value of all columns provided; if you want
per-column normalization, run the tool multiple times instead.*

*Note: this requires reading the entire file into memory.*

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

   $ pdbnormalize -k andthree -- myfile.fsdb

Example output
^^^^^^^^^^^^^^

::

   pdbnormalize -k andthree -- myfile.fsdb
   #fsdb -F t col1:l two andthree:d
   1   key1    0.34146341463414637
   2   key2    1.0
   3   key1    0.7333333333333334

Example normalizing 2 columns:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you normalize multiple columns, be aware that the divisor is the
maximum of all the values from all the columns. Thus by passing both
columns ``col1`` and ``andthree``, you’ll note in the output below that
even col1 is divided by the maximum value from both columns in the input
(*123.0*).

::

   $ pdbnormalize -k col1 andthree -- myfile.fsdb

.. _example-output-1:

Example output
^^^^^^^^^^^^^^

::

   0.008130081300813009    key1    0.34146341463414637
   0.016260162601626018    key2    1.0
   0.024390243902439025    key1    0.7333333333333334


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbnormalize
   :func: parse_args
   :hook:
   :prog: pdbnormalize
