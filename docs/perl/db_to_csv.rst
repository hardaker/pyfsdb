db_to_csv - convert fsdb to the comma-separated-value file-format
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

db_to_csv [-C]

DESCRIPTION
-----------

Covert an existing fsdb file to comma-separated value format.

Input is fsdb format.

Output is CSV-format plain text (*not* fsdb).

OPTIONS
-------

-C or <--omit-comments>
   Also strip all comments.

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

#fsdb -F S paper papertitle reviewer reviewername score1 score2 score3
score4 score5 1 test, paper 2 Smith 4 4 - - - 2 other paper 3 Jones 3 3
- - - 2 input double space 3 Jones 3 3 - - - # \| csv_to_db

Command:
--------

cat data.fsdb \| db_to_csv

Output:
-------

paper,papertitle,reviewer,reviewername,score1,score2,score3,score4,score5
1,"test, paper",2,Smith,4,4,-,-,- 2,"other paper",3,Jones,3,3,-,-,-
2,"input double space",3,Jones,3,3,-,-,- # \| csv_to_db # \| db_to_csv

SEE ALSO
--------

Fsdb. dbfilealter. csv_to_db

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2007-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
