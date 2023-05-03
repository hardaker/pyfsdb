dbsort - sort rows based on the the specified columns
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbsort [-M MemLimit] [-T TemporaryDirectory] [-nNrR] column [column...]

DESCRIPTION
-----------

Sort all input rows as specified by the numeric or lexical columns.

Dbsort consumes a fixed amount of memory regardless of input size. (It
reverts to temporary files on disk if necessary, based on the -M and -T
options.)

The sort should be stable, but this has not yet been verified.

For large inputs (those that spill to disk), dbsort will do some of the
merging in parallel, if possible. The **--parallel** option can control
the degree of parallelism, if desired.

OPTIONS
-------

General option:

-M MaxMemBytes
   Specify an approximate limit on memory usage (in bytes). Larger
   values allow faster sorting because more operations happen in-memory,
   provided you have enough memory.

-T TmpDir
   where to put tmp files. Also uses environment variable TMPDIR, if -T
   is not specified. Default is /tmp.

--parallelism N or -j N
   Allow up to N merges to happen in parallel. Default is the number of
   CPUs in the machine.

Sort specification options (can be interspersed with column names):

-r or --descending
   sort in reverse order (high to low)

-R or --ascending
   sort in normal order (low to high)

-t or --type-inferred-sorting
   sort fields by type (numeric or leicographic), automatically

-T or --no-type-inferred-sorting
   sort fields only as specified based on ``-n`` or ``-N``

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

#fsdb cid cname 10 pascal 11 numanal 12 os

Command:
--------

cat data.fsdb \| dbsort cname

Output:
-------

#fsdb cid cname 11 numanal 12 os 10 pascal # \| dbsort cname

SEE ALSO
--------

**dbmerge** (1), **dbmapreduce** (1), **Fsdb** (3)

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
