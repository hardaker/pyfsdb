dbmultistats - run dbcolstats over each group of inputs identified by
======================================================================


*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

``$0`` [-dm] [-c ConfidencePercent] [-f FormatForm] [-q
NumberOfQuartiles] -k KeyField ValueField

DESCRIPTION
-----------

The input table is grouped by KeyField, then we compute a separate set
of column statistics on ValueField for each group with a unique key.

Assumptions and requirements are the same as dbmapreduce (this program
is just a wrapper around that program):

By default, data can be provided in arbitrary order and the program
consumes O(number of unique tags) memory, and O(size of data) disk
space.

With the -S option, data must arrive group by tags (not necessarily
sorted), and the program consumes O(number of tags) memory and no disk
space. The program will check and abort if this precondition is not met.

With two -S's, program consumes O(1) memory, but doesn't verify that the
data-arrival precondition is met.

(Note that these semantics are exactly like dbmapreduce -k KeyField Ω-
dbcolstats ValueField dbmultistats provides a simpler API that passes
through statistics-specific arguments and is optimized when data is
pre-sorted and there are no quarties or medians.)

OPTIONS
-------

Options are the same as dbcolstats.

-k or --key KeyField
   specify which column is the key for grouping (default: the first
   column)

--output-on-no-input
   Enables null output (all fields are -, n is 0) if we get input with a
   schema but no records. Without this option, just output the schema
   but no rows. Default: no output if no input.

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

-S or --pre-sorted
   Assume data is already sorted. With one -S, we check and confirm this
   precondition. When repeated, we skip the check.

-T TmpDir
   where to put temporary data. Only used if median or quantiles are
   requested. Also uses environment variable TMPDIR, if -T is not
   specified. Default is /tmp.

--parallelism=N or -j N
   Allow up to N reducers to run in parallel. Default is the number of
   CPUs in the machine.

-F or --fs or --fieldseparator S
   Specify the field (column) separator as ``S``. See dbfilealter for
   valid field separators.

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

#fsdb experiment duration ufs_mab_sys 37.2 ufs_mab_sys 37.3 ufs_rcp_real
264.5 ufs_rcp_real 277.9

Command:
--------

cat DATA/stats.fsdb \| dbmultistats -k experiment duration

Output:
-------

#fsdb experiment mean stddev pct_rsd conf_range conf_low conf_high
conf_pct sum sum_squared min max n ufs_mab_sys 37.25 0.070711 0.18983
0.6353 36.615 37.885 0.95 74.5 2775.1 37.2 37.3 2 ufs_rcp_real 271.2
9.4752 3.4938 85.13 186.07 356.33 0.95 542.4 1.4719e+05 264.5 277.9 2 #
\| /home/johnh/BIN/DB/dbmultistats experiment duration

SEE ALSO
--------

Fsdb. dbmapreduce. dbcolstats.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2015 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
