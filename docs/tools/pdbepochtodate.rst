pdbepochtodate - translate a unix epoch column to a date-string column
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdbepochtodante`` translates a column containing unix epoch seconds
(since Jan 1 1970) to another column with a formatted date/time. This
tool is the inverse of the ``pdbdatetoepoch`` tool. .

Example input (*myepoch.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F t index:l timestamp:d
   1   1672560000
   2   1678831200

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdbepochtodante -d datecol -t timestamp percent mytime.fsdb

Example output
^^^^^^^^^^^^^^

::

   #fsdb -F t index:l timestamp:d date
   1   1672560000.0    2023-01-01 00:00
   2   1678831200.0    2023-03-14 15:00

Notes
^^^^^

Internally this uses python’s ``dateparser`` module.


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdbepochtodate
   :func: parse_args
   :hook:
   :prog: pdbepochtodate
