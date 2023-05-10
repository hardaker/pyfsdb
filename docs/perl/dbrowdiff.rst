dbrowdiff - compute row-by-row differences of some column
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbrowdiff [-B|-I] column

DESCRIPTION
-----------

For a given column, compute the differences between each row of the
table. Differences are output to two new columns, ``absdiff`` and
``pctdiff``.

Differences are either relative to the previous column (*incremental*
mode), or relative to the first row (*baseline* mode), the default.

OPTIONS
-------

-B or --baseline
   Select baseline mode (the default), where differences are relative to
   the first row.

-I or --incremental
   Select incremental mode, where differences are relative to the
   previous row.

-f FORMAT or --format FORMAT
   Specify a **printf** (3)-style format for output statistics. Defaults
   to ``%.5g``.

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

#fsdb event clock:d \_null_getpage+128 815812813.281756
\_null_getpage+128 815812813.328709 \_null_getpage+128 815812813.353830
\_null_getpage+128 815812813.357169 \_null_getpage+128 815812813.375844
\_null_getpage+128 815812813.378358 # \| /home/johnh/BIN/DB/dbrow # \|
/home/johnh/BIN/DB/dbcol event clock

Command:
--------

cat DATA/kitrace.fsdb \| dbrowdiff clock

Output:
-------

#fsdb event clock:d absdiff:d pctdiff:d \_null_getpage+128
815812813.281756 0 0 \_null_getpage+128 815812813.328709 0.046953
5.7554e-09 \_null_getpage+128 815812813.353830 0.072074 8.8346e-09
\_null_getpage+128 815812813.357169 0.075413 9.2439e-09
\_null_getpage+128 815812813.375844 0.094088 1.1533e-08
\_null_getpage+128 815812813.378358 0.096602 1.1841e-08 # \|
/home/johnh/BIN/DB/dbrow # \| /home/johnh/BIN/DB/dbcol event clock # \|
dbrowdiff clock

SEE ALSO
--------

Fsdb. dbcolmovingstats. dbrowuniq. dbfilediff.

dbrowdiff, dbrowuniq, and dbfilediff are similar but different.
dbrowdiff computes row-by-row differences for a column, dbrowuniq
eliminates rows that have no differences, and dbfilediff compares fields
of two files.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
