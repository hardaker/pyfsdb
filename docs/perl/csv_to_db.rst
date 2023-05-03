csv_to_db - convert comma-separated-value data into fsdb
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

csv_to_db <source.csv

DESCRIPTION
-----------

Converts a comma-separated-value data stream to Fsdb format.

The input is CSV-format (*not* fsdb). The first row is taken to be the
names of the columns.

The output is two-space-separated fsdb. (Someday more general field
separators should be supported.) Fsdb fields are normalized version of
the CSV file: spaces are converted to single underscores.

OPTIONS
-------

-F or --fs or --fieldseparator S
   Specify the field (column) separator as ``S``. See dbfilealter for
   valid field separators. Default is S (double space).

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

paper,papertitle,reviewer,reviewername,score1,score2,score3,score4,score5
1,"test, paper",2,Smith,4,4,,, 2,other paper,3,Jones,3,3,,,

Command:
--------

csv_to_db

Output:
-------

#fsdb -F S paper papertitle reviewer reviewername score1 score2 score3
score4 score5 1 test, paper 2 Smith 4 4 - - - 2 other paper 3 Jones 3 3
- - - # \| csv_to_db

SEE ALSO
--------

Fsdb. db_to_csv.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2008 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
