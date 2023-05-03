dbcolhisto - compute a histogram over a column of Fsdb data
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbcolhisto [-ag] [-W BucketWidth] [-S BucketStart] [-E BucketEnd] [-N
NumberOfBuckets] column

DESCRIPTION
-----------

This program computes a histogram over a column of data. Records
containing non-numeric data are considered null do not contribute to the
stats (optionally they are treated as zeros).

Defaults to 10 buckets over the exact range of data. Up to three
parameters (number of buckets, start, end, and width) can be specified,
the rest default accordingly.

Buckets range from a value (given the the low column) to just below the
next low value and buckets are equal width. If necessary, extra <min and
>max buckets are created. By default, the last bucket includes max (and
is thus infinitesimally larger than the other buckets). This
irregularity can be removed with the ``-I`` option.

This program requires O(number of buckets) memory and O(size of data)
temporary disk space.

OPTIONS
-------

-W or --width N
   Gives with width of each bucket, in data units. Default is whatever
   gives 10 buckets over the whole range of data.

-S or --start N
   Buckets start at value N, in data units. Default is the minimum data
   value.

-E or --end N
   Buckets end at value N, in data units. Default is the maximum data
   value.

-N or --number N
   Create N buckets. The default is 10 buckets.

-g or --graphical
   Generate a graphical histogram (with asterisks). Default is numeric.

-I or --last-inclusive
   Make the last bucket non-inclusive of the last value.

-a
   Compute stats over all records (treat non-numeric records as zero
   rather than just ignoring them). Default is non-numeric records are
   ignored.

-e EmptyValue or --empty
   Specify the value any null bins get. (Default: -.)

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

#fsdb name id test1 a 1 80 b 2 70 c 3 65 d 4 90 e 5 70 f 6 90

Command:
--------

cat DATA/grades.fsdb \| dbcolhisto -S 0 -E 100 -N 10 test1

Output:
-------

#fsdb low histogram:q 0 0 10 0 20 0 30 0 40 0 50 0 60 1 70 2 80 1 90 2 #
\| dbcolhisto -S 0 -E 100 -N 10 test1

SEE ALSO
--------

Fsdb, dbcolpercentile, dbcolstats

BUGS
----

This program could run in constant memory with no external storage when
the buckets are pre-specified. That optimization is not implemented.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
