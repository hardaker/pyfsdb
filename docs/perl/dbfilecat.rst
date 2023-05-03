dbfilecat - concatenate two files with identical schema
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbfilecat --input A.fsdb [--input B.fsdb...]

or

echo A.fsdb \| dbfilecat --xargs

DESCRIPTION
-----------

Concatenate all provided input files, producing one result. We remove
extra header lines.

Inputs can both be specified with ``--input``, or one can come from
standard input and the other from ``--input``. With ``--xargs``, each
line of standard input is a filename for input.

Inputs must have identical schemas (columns, column order, and field
separators).

Like dbmerge, but no worries about sorting, and with no arguments we
read standard input (although that's not very useful).

OPTIONS
-------

General option:

--xargs
   Expect that input filenames are given, one-per-line, on standard
   input. (In this case, merging can start incrementally.

--removeinputs
   Delete the source files after they have been consumed. (Defaults off,
   leaving the inputs in place.) This module also supports the standard
   fsdb options:

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

File *a.fsdb*:

#fsdb cid cname 11 numanal 10 pascal

File *b.fsdb*:

#fsdb cid cname 12 os 13 statistics

Command:
--------

dbfilecat --input a.fsdb --input b.fsdb

Output:
-------

#fsdb cid cname 11 numanal 10 pascal 12 os 13 statistics # \| dbmerge
--input a.fsdb --input b.fsdb

SEE ALSO
--------

**dbmerge** (1), **Fsdb** (3)

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2013-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
