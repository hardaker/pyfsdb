dbmerge2 - merge exactly two inputs in sorted order based on the the
======================================================================


*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbmerge2 --input A.fsdb --input B.fsdb [-T TemporaryDirectory] [-nNrR]
column [column...]

or cat A.fsdb \| dbmerge2 --input B.fsdb [-T TemporaryDirectory] [-nNrR]
column [column...]

DESCRIPTION
-----------

Merge exactly two sorted input files, producing one sorted result.
Inputs can both be specified with ``--input``, or one can come from
standard input and the other from ``--input``.

Inputs must have identical schemas (columns, column order, and field
separators).

Dbmerge2 consumes a fixed amount of memory regardless of input size.

Although described above as a command line too, the command line version
of dbmerge2 is not installed by default. Dbmerge2 is used primarily
internal to perl; **dbmerge** (1) is the command-line tool for user use.

Warning: we do not verify that each input is actually sorted. In correct
merge results will occur if they are not.

OPTIONS
-------

General option:

--saveoutput $OUT_REF
   Save output writer (for integration with other fsdb filters).

<-T TmpDir>
   where to put tmp files. Also uses environment variable TMPDIR, if -T
   is not specified. Default is /tmp.

Sort specification options (can be interspersed with column names):

-r or --descending
   sort in reverse order (high to low)

-R or --ascending
   sort in normal order (low to high)

-n or --numeric
   sort numerically

-N or --lexical
   sort lexicographically

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

File *a.fsdb*:

#fsdb cid cname 11 numanal 10 pascal

File *b.fsdb*:

#fsdb cid cname 12 os 13 statistics

Command:
--------

dbmerge2 --input a.fsdb --input b.fsdb cname

or

cat a.fsdb \| dbmerge2 --input b.fsdb cname

Output:
-------

#fsdb cid cname 11 numanal 12 os 10 pascal 13 statistics # \| dbmerge2
--input a.fsdb --input b.fsdb cname

SEE ALSO
--------

**dbmerge** (1), **dbsort** (1), **Fsdb** (3)

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
