dbmerge - merge all inputs in sorted order based on the the specified
======================================================================


*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbmerge --input A.fsdb --input B.fsdb [-T TemporaryDirectory] [-nNrR]
column [column...]

or cat A.fsdb \| dbmerge --input - --input B.fsdb [-T
TemporaryDirectory] [-nNrR] column [column...]

or dbmerge [-T TemporaryDirectory] [-nNrR] column [column...] --inputs
A.fsdb [B.fsdb ...]

or { echo A.fsdb; echo B.fsdb } \| dbmerge --xargs column [column...]

DESCRIPTION
-----------

Merge all provided, pre-sorted input files, producing one sorted result.
Inputs can both be specified with ``--input``, or with ``--inputs``, or
one can come from standard input and the other from ``--input``. With
``--xargs``, each line of standard input is a filename for input.

Inputs must have identical schemas (columns, column order, and field
separators).

Unlike *dbmerge2*, *dbmerge* supports an arbitrary number of input
files.

Because this program is intended to merge multiple sources, it does
*not* default to reading from standard input. If you wish to read
standard input, giv *-* as an explicit input source.

Also, because we deal with multiple input files, this module doesn't
output anything until it's run.

dbmerge consumes a fixed amount of memory regardless of input size. It
therefore buffers output on disk as necessary. (Merging is implemented a
series of two-way merges and possibly an n-way merge at the end, so disk
space is O(number of records).)

dbmerge will merge data in parallel, if possible. The ``--parallelism``
option can control the degree of parallelism, if desired.

OPTIONS
-------

General option:

--xargs
   Expect that input filenames are given, one-per-line, on standard
   input. (In this case, merging can start incrementally.)

--removeinputs
   Delete the source files after they have been consumed. (Defaults off,
   leaving the inputs in place.)

-T TmpDir
   where to put tmp files. Also uses environment variable TMPDIR, if -T
   is not specified. Default is /tmp.

--parallelism N or -j N
   Allow up to N merges to happen in parallel. Default is the number of
   CPUs in the machine.

--endgame (or --noendgame)
   Enable endgame mode, extra parallelism when finishing up. (On by
   default.)

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

These two files are both sorted by ``cname``, and they have identical
schemas.

Command:
--------

dbmerge --input a.fsdb --input b.fsdb cname

or

cat a.fsdb \| dbmerge --input b.fsdb cname

Output:
-------

#fsdb cid cname 11 numanal 12 os 10 pascal 13 statistics # \| dbmerge
--input a.fsdb --input b.fsdb cname

SEE ALSO
--------

**dbmerge2** (1), **dbsort** (1), **Fsdb** (3)

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2020 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
