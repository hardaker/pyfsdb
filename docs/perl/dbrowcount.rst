dbrowcount - count the number of rows in an Fsdb stream
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbrowcount

DESCRIPTION
-----------

Count the number of rows and write out a new fsdb file with one column
(n) and one value: the number of rows. This program is a strict subset
of dbcolstats.

Although there are other ways to get a count of rows (``dbcolstats``, or
``dbrowaccumulate -C 1`` and some processing), counting is so common it
warrants its own command. (For example, consider how often ``wc -l`` is
used in regular shell scripting.) There are some gross and subtle
differences, though, in that ``dbrowcount`` doesn't require one to
specify a column to search, and it also doesn't look for and skip null
data items.

OPTIONS
-------

No program-specific options.

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

#fsdb absdiff 0 0.046953 0.072074 0.075413 0.094088 0.096602 # \|
/home/johnh/BIN/DB/dbrow # \| /home/johnh/BIN/DB/dbcol event clock # \|
dbrowdiff clock # \| /home/johnh/BIN/DB/dbcol absdiff

Command:
--------

cat data.fsdb \| dbrowcount

Output:
-------

#fsdb n 6 # \| /home/johnh/BIN/DB/dbrow # \| /home/johnh/BIN/DB/dbcol
event clock # \| dbrowdiff clock # \| /home/johnh/BIN/DB/dbcol absdiff

Input 2:
--------

As another example, this input produces the same output as above in
``dbrowcount``, but different output in ``dbstats``:

#fsdb absdiff - - - - - - # \| /home/johnh/BIN/DB/dbrow # \|
/home/johnh/BIN/DB/dbcol event clock # \| dbrowdiff clock # \|
/home/johnh/BIN/DB/dbcol absdiff

SEE ALSO
--------

**dbcolaccumulate** (1), **dbcolstats** (1), **Fsdb** (3)

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2007-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
