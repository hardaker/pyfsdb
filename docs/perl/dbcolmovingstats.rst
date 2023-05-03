dbcolmovingstats - compute moving statistics over a window of a column
======================================================================


*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolmovingstats [-am] [-w WINDOW] [-e EmptyValue] [-k KEY] column

DESCRIPTION
-----------

Compute moving statistics over a COLUMN of data. Records containing
non-numeric data are considered null do not contribute to the stats
(optionally they are treated as zeros with ``-a``).

Statitics are computed over a WINDOW of samples of data.

[In progress 2020-11-12, but not completed: Alternatively, if a key
column is given with ``-k KEY``, then a we treat the key column as a
time value and compute the time-weighted mean.]

Currently we compute mean and sample standard deviation. (Note we only
compute sample standard deviation, not full population.) Optionally,
with ``-m`` we also compute median. (Currently there is no support for
generalized quantiles.)

Values before a sufficient number have been accumulated are given the
empty value (if specified with ``-e``). If no empty value is given,
stats are computed on as many are possible if no empty value is
specified.

Dbcolmovingstats runs in O(1) memory, but must buffer a full window of
data. Quantiles currently will repeatedly sort the window and so may
perform poorly with wide windows.

OPTIONS
-------

-a or --include-non-numeric
   Compute stats over all records (treat non-numeric records as zero
   rather than just ignoring them).

-w or --window WINDOW
   WINDOW of how many items to accumulate (defaults to 10). (For
   compatibility with fsdb-1.x, **-n** is also supported.)

-k or --key KEY
   The KEY specifies a field that is used to evaluate the window---a
   window must span at most this range of value so the key field. (For
   example, if KEY is the time and window is 60, then enough samples
   will be added to make at most 60s of observations. With a key,
   sampling can be irregular.) If key is specified, we also output a
   moving_n field for how many samples are in each window.

-m or --median
   Show median of the window in addition to mean.

-e E or --empty E
   Give value E as the value for empty (null) records. This null value
   is then output before a full window is accumulated.

-f FORMAT or --format FORMAT
   Specify a **printf** (3)-style format for output mean and standard
   deviation. Defaults to ``%.5g``.

Eventually we expect to support other options of dbcolstats.

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

#fsdb date epoch count 19980201 886320000 6 19980202 886406400 8
19980203 886492800 19 19980204 886579200 53 19980205 886665600 20
19980206 886752000 18 19980207 886838400 5 19980208 886924800 9 19980209
887011200 22 19980210 887097600 22 19980211 887184000 36 19980212
887270400 26 19980213 887356800 23 19980214 887443200 6

Command:
--------

cat data.fsdb \| dbmovingstats -e - -w 4 count

Output:
-------

#fsdb date epoch count moving_mean moving_stddev 19980201 886320000 6 -
- 19980202 886406400 8 - - 19980203 886492800 19 - - 19980204 886579200
53 21.5 21.764 19980205 886665600 20 25 19.442 19980206 886752000 18
27.5 17.02 19980207 886838400 5 24 20.445 19980208 886924800 9 13 7.1647
19980209 887011200 22 13.5 7.8528 19980210 887097600 22 14.5 8.8129
19980211 887184000 36 22.25 11.026 19980212 887270400 26 26.5 6.6081
19980213 887356800 23 26.75 6.3966 19980214 887443200 6 22.75 12.473 #
\| dbcolmovingstats -e - -n 4 count

SEE ALSO
--------

Fsdb. dbcolstats. dbmultistats. dbrowdiff.

BUGS
----

Currently there is no support for generalized quantiles.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
