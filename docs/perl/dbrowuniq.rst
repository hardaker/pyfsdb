dbrowuniq - eliminate adjacent rows with duplicate fields, maybe
======================================================================


*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbrowuniq [-cFLB] [uniquifying fields...]

DESCRIPTION
-----------

Eliminate adjacent rows with duplicate fields, perhaps counting them.
Roughly equivalent to the Unix uniq command, but optionally only
operating on the specified fields.

By default, *all* columns must be unique. If column names are specified,
only those columns must be unique and the first row with those columns
is returned.

Dbrowuniq eliminates only identical rows that *adjacent*. If you want to
eliminate identical rows across the entirefile, you must make them
adajcent, perhaps by using dbsort on your uniquifying field. (That is,
the input with three lines a/b/a will produce three lines of output with
both a's, but if you dbsort it, it will become a/a/b and dbrowuniq will
output a/b.

By default, dbrowuniq outputs the *first* unique row. Optionally, with
``-L``, it will output the *last* unique row, or with ``-B`` it outputs
both first and last. (This choice only matters when uniqueness is
determined by specific fields.)

dbrowuniq can also count how many unique, adjacent lines it finds with
``-c``, with the count going to a new column (defaulting to ``count``).
Incremental counting, when the ``count`` column already exists, is
possible with ``-I``. With incremental counting, the existing count
column is summed.

OPTIONS
-------

-c or --count
   Create a new column (count) which counts the number of times each
   line occurred. The new column is named by the ``-N`` argument,
   defaulting to ``count``.

-N on --new-name
   Specify the name of the count column, if any. Please specify the type
   with the name, if desired (allowing one to pick sizes smaller than
   the default quad, if desired). (Default is ``count:q``.)

-I on --incremental
   Incremental counting. If the count column exists, it is assumed to
   have a partial count and the count accumulates. If the count column
   doesn't exist, it is created.

-L or --last
   Output the last unique row only. By default, it outputs the first
   unique row.

-F or --first
   Output the first unique row only. (This output is the default.)

-B or --both
   Output both the first and last unique rows.

This module also supports the standard fsdb options:

-d
   Enable debugging output.

-i or --input InputSource
   Read from InputSource, typically a file name, or ``-`` for standard
   input, or (if in Perl) a IO::Handle, Fsdb::IO or Fsdb::BoundedQueue
   objects.

-o or --output OutputDestination
   Write to OutputDestination, typically a file name, or ``-`` for
   standard output, or (if in Perl) a IO::Handle, Fsdb::IO or
   Fsdb::BoundedQueue objects.

--autorun or --noautorun
   By default, programs process automatically, but Fsdb::Filter objects
   in Perl do not run until you invoke the **run()** method. The
   ``--(no)autorun`` option controls that behavior within Perl.

--header H
   Use H as the full Fsdb header, rather than reading a header from then
   input.

--help
   Show help.

--man
   Show full manual.

SAMPLE USAGE
------------

Input:
------

#fsdb event \_null_getpage+128 \_null_getpage+128 \_null_getpage+128
\_null_getpage+128 \_null_getpage+128 \_null_getpage+128
\_null_getpage+4 \_null_getpage+4 \_null_getpage+4 \_null_getpage+4
\_null_getpage+4 \_null_getpage+4 # \| /home/johnh/BIN/DB/dbcol event #
\| /home/johnh/BIN/DB/dbsort event

Command:
--------

cat data.fsdb \| dbrowuniq -c

Output:
-------

#fsdb event count \_null_getpage+128 6 \_null_getpage+4 6 # 2
/home/johnh/BIN/DB/dbcol event # \| /home/johnh/BIN/DB/dbrowuniq -c

SAMPLE USAGE 2
--------------

Retaining the last unique row as an example.

Input:
------

#fsdb event i \_null_getpage+128 10 \_null_getpage+128 11
\_null_getpage+128 12 \_null_getpage+128 13 \_null_getpage+128 14
\_null_getpage+128 15 \_null_getpage+4 16 \_null_getpage+4 17
\_null_getpage+4 18 \_null_getpage+4 19 \_null_getpage+4 20
\_null_getpage+4 21 # \| /home/johnh/BIN/DB/dbcol event # \|
/home/johnh/BIN/DB/dbsort event

Command:
--------

cat data.fsdb \| dbrowuniq -c -L event

Output:
-------

#fsdb event i count \_null_getpage+128 15 6 # \|
/home/johnh/BIN/DB/dbcol event # \| /home/johnh/BIN/DB/dbsort event
\_null_getpage+4 21 6 # \| dbrowuniq -c

SAMPLE USAGE 3
--------------

Incremental counting.

Input:
------

#fsdb event count \_null_getpage+128 6 \_null_getpage+128 6
\_null_getpage+4 6 \_null_getpage+4 6 # /home/johnh/BIN/DB/dbcol event #
\| /home/johnh/BIN/DB/dbrowuniq -c

Command:
--------

cat data.fsdb \| dbrowuniq -I -c event

Output:
-------

#fsdb event count \_null_getpage+128 12 \_null_getpage+4 12 #
/home/johnh/BIN/DB/dbcol event # \| /home/johnh/BIN/DB/dbrowuniq -c # \|
dbrowuniq -I -c event

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1997-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
