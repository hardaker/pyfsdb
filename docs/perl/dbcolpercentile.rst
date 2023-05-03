dbcolpercentile - compute percentiles or ranks for an existing numeric
======================================================================


*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolpercentile [-rplhS] [--mode MODE] [--value WEIGHT_COL] column

DESCRIPTION
-----------

Compute a percentile, ranking, or weighted percentile of a column of
numbers. The new column will be called *percentile:d* or *rank:q* or
*weighted:d* depending on the mode.

Ordering is given by the specifed column.

In weighted mode, by default the same column as ordering is used for
weighting. Alternatively, give a different column for weighting with
``-v``.

Non-numeric values are ignored.

If the data is pre-sorted and only a rank is requested, no extra storage
is required. In all other cases, a full copy of data is buffered on
disk. Output will be sorted by COLUMN.

OPTIONS
-------

-p or --percentile or --mode percentile
   Show percentile (default). Percentile is the fraction of the
   cumulative values at or lower than the current value, relative to the
   total count.

-P or --rank or --nopercentile or --mode rank
   Compute ranks instead of percentiles.

-w WEIGHT_COL or --weighted WEIGHT_COL or --mode weighted
   Compute the weighted percentile. Here values define not only the
   ordering, but the fraction of the total sum, and percentile is the
   fraction of sum of cumulative values in the weighting column
   (relative to their sum), for all ranking colums at or lower than the
   current ranking column. If the weight column is not specified (with
   ``--mode weighted``), it is the same as the ranking column.

-a or --include-non-numeric
   Compute stats over all records (treat non-numeric records as zero
   rather than just ignoring them).

-S or --pre-sorted
   Assume data is already sorted. With one -S, we check and confirm this
   precondition. When repeated, we skip the check.

-N NAME or --new-name NAME
   Give the NAME of the new column. (If no type is specifed, a type will
   be assigned based on the mode.)

-f FORMAT or --format FORMAT
   Specify a **printf** (3)-style format for output statistics. Defaults
   to ``%.5g``.

-T TmpDir
   where to put tmp files. Also uses environment variable TMPDIR, if -T
   is not specified. Default is /tmp.

-e EmptyValue or --empty
   Specify the value any non-numeric rows get, if in weighted mode.

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

cat DATA/grades.fsdb \| dbcolpercentile test1

Output:
-------

#fsdb name id test1 percentile d 4 90 1 f 6 90 1 a 1 80 0.66667 b 2 70
0.5 e 5 70 0.5 c 3 65 0.16667 # \| dbsort -n test1 # \| dbcolpercentile
test1

Command 2:
----------

cat DATA/grades.fsdb \| dbcolpercentile --rank test1

Output 2:
---------

#fsdb name id test1 rank d 4 90 1 f 6 90 1 a 1 80 3 b 2 70 4 e 5 70 4 c
3 65 6 # \| dbsort -n test1 # \| dbcolpercentile --rank test1

SEE ALSO
--------

Fsdb. dbcolhisto.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
