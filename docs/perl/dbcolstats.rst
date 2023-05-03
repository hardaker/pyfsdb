dbcolstats - compute statistics on a fsdb column
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolstats [-amS] [-c ConfidenceFraction] [-q NumberOfQuantiles] column

DESCRIPTION
-----------

Compute statistics over a COLUMN of data. Records containing non-numeric
data are considered null do not contribute to the stats (with the ``-a``
option they are treated as zeros).

Confidence intervals are a t-test (+/- (t_{a/2})*s/sqrt(n)) and assume
the population takes a normal distribution with a small number of
samples (< 100).

By default, all statistics are computed for as a population *sample*
(with an \``n-1'' term), not as representing the whole population (using
\``n''). Select between them with **--sample** or **--nosample**. When
you measure the entire population, use the latter option.

The output of this program is probably best looked at after reformatting
with dblistize.

Dbcolstats runs in O(1) memory. Median or quantile requires sorting the
data and invokes dbsort. Sorting will run in constant RAM but O(number
of records) disk space. If median or quantile is required and the data
is already sorted, dbcolstats will run more efficiently with the -S
option.

OPTIONS
-------

-a or --include-non-numeric
   Compute stats over all records (treat non-numeric records as zero
   rather than just ignoring them).

-c FRACTION or --confidence FRACTION
   Specify FRACTION for the confidence interval. Defaults to 0.95 for a
   95% confidence factor.

-f FORMAT or --format FORMAT
   Specify a **printf** (3)-style format for output statistics. Defaults
   to ``%.5g``.

-m or --median
   Compute median value. (Will sort data if necessary.) (Median is the
   quantitle for N=2.)

-q N or --quantile N
   Compute quantile (quartile when N is 4), or an arbitrary quantile for
   other values of N, where the scores that are 1 Nth of the way across
   the population.

--sample
   Compute *sample* population statistics (e.g., the sample standard
   deviation), assuming *n-1* degrees of freedom.

--nosample
   Compute *whole* population statistics (e.g., the population standard
   devation).

-S or --pre-sorted
   Assume data is already sorted. With one -S, we check and confirm this
   precondition. When repeated, we skip the check. (This flag is ignored
   if quartiles are not requested.)

--parallelism=N or "-j N"
   Allow sorting to happen in parallel. Defaults on. (Only relevant if
   using non-pre-sorted data with quantiles.)

-F or --fs or --fieldseparator S
   Specify the field (column) separator as ``S``. See dbfilealter for
   valid field separators.

-T TmpDir
   where to put temporary data. Only used if median or quantiles are
   requested. Also uses environment variable TMPDIR, if -T is not
   specified. Default is /tmp.

-k KeyField
   Do multi-stats, grouped by each key. Assumes keys are sorted. (Use
   dbmultistats to guarantee sorting order.)

--output-on-no-input
   Enables null output (all fields are -, n is 0) if we get input with a
   schema but no records. Without this option, just output the schema
   but no rows. Default: no output if no input.

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

cat data.fsdb \| dbcolstats absdiff

Output:
-------

#fsdb mean:d stddev:d pct_rsd:d conf_range:d conf_low:d conf_high:d
conf_pct:d sum:d sum_squared:d min:d max:d n:q 0.064188 0.036194 56.387
0.037989 0.026199 0.102180.95 0.38513 0.031271 0 0.096602 6 # \|
/home/johnh/BIN/DB/dbrow # \| /home/johnh/BIN/DB/dbcol event clock # \|
dbrowdiff clock # \| /home/johnh/BIN/DB/dbcol absdiff # \| dbcolstats
absdiff # 0.95 confidence intervals assume normal distribution and small
n.

SEE ALSO
--------

**dbmultistats** (1), handles multiple experiments in a single file.

**dblistize** (1), to pretty-print the output of dbcolstats.

**dbcolpercentile** (1), to compute an even more general version of
median/quantiles.

**dbcolstatscores** (1), to compute z-scores or t-scores for each row

**dbrvstatdiff** (1), to see if two sample populations are statistically
different.

Fsdb.

BUGS
----

The algorithms used to compute variance have not been audited to check
for numerical stability. (See
*http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance*).)
Variance may be incorrect when standard deviation is small relative to
the mean.

The field ``conf_pct`` implies percentage, but it's actually reported as
a fraction (0.95 means 95%).

Because of limits of floating point, statistics on numbers of widely
different scales may be incorrect. See the test cases
*dbcolstats_extrema* for examples.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
