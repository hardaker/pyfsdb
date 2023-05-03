dbrowaccumulate - compute a running sum of a column
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbrowaccumulate [-C increment_constant] [-I initial_value] [-c
increment_column] [-N new_column_name]

DESCRIPTION
-----------

Compute a running sum over a column of data, or of a constant
incremented per row, perhaps to generate a cumulative distribution.

What to accumulate is specified by ``-c`` or ``-C``.

The new column is named by the ``-N`` argument, defaulting to ``accum``.

OPTIONS
-------

-c or --column COLUMN
   Accumulate values from the given COLUMN. No default.

-C or --constant K
   Accumulate the given constant K for each row of input. No default.

-I or --initial-value I
   Start accumulation at value I. Defaults to zero.

-N or --new-name N
   Name the new column N. Defaults to ``accum``.

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

--help
   Show help.

--man
   Show full manual.

SAMPLE USAGE
------------

Input:
------

#fsdb diff 0.0 00.000938 00.001611 00.001736 00.002006 00.002049 # \|
/home/johnh/BIN/DB/dbrow # \| /home/johnh/BIN/DB/dbcol diff # \| dbsort
diff

Command:
--------

cat DATA/kitrace.fsdb \| dbrowaccumulate -c diff

Output:
-------

#fsdb diff accum 0.0 0 00.000938 .000938 00.001611 .002549 00.001736
.004285 00.002006 .006291 00.002049 .00834 # \| /home/johnh/BIN/DB/dbrow
# \| /home/johnh/BIN/DB/dbcol diff # \| dbsort diff # \|
/home/johnh/BIN/DB/dbrowaccumulate diff

SEE ALSO
--------

Fsdb, dbrowenumerate.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
