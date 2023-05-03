pdb2tex - create a latex table using the data in a FSDB file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdb2tex`` converts an FSDB file into a latex table/tabular output

Example input (*myfile.fsdb*):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   #fsdb -F t col1:l two:a andthree:d
   1   key1    42.0
   2   key2    123.0
   3   key1    90.2

Example command usage
^^^^^^^^^^^^^^^^^^^^^

::

   $ pdb2tex myfile.fsdb 

Example output
^^^^^^^^^^^^^^

.. code:: latex

   \begin{table}
     \begin{tabular}{lll}
       \textbf{col1} & \textbf{two} & \textbf{andthree} \\
       1 & key1 & 42.0 \\
       2 & key2 & 123.0 \\
       3 & key1 & 90.2 \\
     \end{tabular}
   \end{table}


Command Line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. sphinx_argparse_cli::
   :module: pyfsdb.tools.pdb2tex
   :func: parse_args
   :hook:
   :prog: pdb2tex
