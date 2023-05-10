dbfilediff - compare two fsdb tables
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbfilediff [-Eq] [-N diff_column_name] --input table1.fsdb --input
table2.fsdb

OR

cat table1.fsdb \| dbfilediff [-sq] --input table2.fsdb

DESCRIPTION
-----------

Dbfilediff compares two Fsdb tables, row by row. Unlike Unix
**diff** (1), this program assumes the files are identical line-by-line
and we compare fields. Thus, insertion of one extra row will result in
all subsequent lines being marked different.

By default, *all* columns must be unique. (At some point, support to
specific specific columns may be added.)

Output is a new table with a new column ``diff`` (or something else if
the ``-N`` option is given), - and + for the first and second non-equal
rows, = for matching lines, or ~ if they are equal with epsilon numerics
(in which case only the second row is included). Unlike Unix
**diff** (1), we output *all* rows (the = lines), not just diffs (the
``--quiet`` option suppresses this output).

Optionally, with ``-E`` it will do a epsilon numeric comparision, to
account for things like variations in different computer's floating
point precision and differences in printf output.

Epsilon comparision is asymmetric, in that it assumes the first input is
correct an allows the second input to vary, but not the reverse.

Because two tables are required, input is typically in files. Standard
input is accessible by the file -.

OPTIONS
-------

-E or --epsilon
   Do epsilon-numeric comparison. (Described above.) Epsilon-comparision
   is only done on columns that look like floating point numbers, not on
   strings or integers. Epsilon comparision allows the last digit to
   vary by 1, or for there to be one extra digit of precision, but only
   for floating point numbers. Rows that are within epsilon are not
   considered different for purposes of the exit code.

--exit
   Exit with a status of 1 if some differences were found. (By default,
   the exit status is 0 with or without differences if the file is
   processed successfully.)

-N on --new-name
   Specify the name of the ``diff`` column, if any. (Default is
   ``diff``.)

-q or --quiet
   Be quiet, suppressing output for identical rows. (This behavior is
   different from Unix **diff** (1) where ``-q`` suppresses *all*
   output.) If repeated, omits epsilon-equivalent rows.

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

#fsdb event clock absdiff pctdiff \_null_getpage+128 815812813.281756 0
0 \_null_getpage+128 815812813.328709 0.046953 5.7554e-09
\_null_getpage+128 815812813.353830 0.025121 3.0793e-09
\_null_getpage+128 815812813.357169 0.0033391 4.0929e-10

And in the file *TEST/dbfilediff_ex.in-2*:

#fsdb event clock absdiff pctdiff \_null_getpage+128 815812813.281756 0
0 \_null_getpage+128 815812813.328709 0.046953 5.7554e-09
\_null_getpage+128 815812813.353830 0.025121 3.0793e-09
\_null_getpage+128 815812813.357169 0.003339 4.0929e-10

Command:
--------

cat TEST/dbfilediff_ex.in \| dbfilediff -i - -i TEST/dbfilediff_ex.in-2

Output:
-------

#fsdb event clock absdiff pctdiff diff \_null_getpage+128
815812813.281756 0 0 = \_null_getpage+128 815812813.328709 0.046953
5.7554e-09 = \_null_getpage+128 815812813.353830 0.025121 3.0793e-09 =
\_null_getpage+128 815812813.357169 0.0033391 4.0929e-10 -
\_null_getpage+128 815812813.357169 0.003339 4.0929e-10 + # \|
dbfilediff --input TEST/dbfilediff_ex.in-2

By comparision, if one adds the ``-s`` option, then all rows will pass
as equal.

SEE ALSO
--------

Fsdb. dbrowuniq. dbfilediff.

dbrowdiff, dbrowuniq, and dbfilediff are similar but different.
dbrowdiff computes row-by-row differences for a column, dbrowuniq
eliminates rows that have no differences, and dbfilediff compares fields
of two files.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2012-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
