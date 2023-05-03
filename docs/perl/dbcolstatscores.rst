dbcolstatscores - compute z-scores or t-scores for each value in a
======================================================================


*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolstatscores [-t] [--tmean=MEAN] [--tstddev=STDDEV] column

DESCRIPTION
-----------

Compute statistics (z-score and optionally t-score) over a COLUMN of
numbers. Creates new columns called zscore, tscore. T-scores are only
computed if requested with the ``-t`` option, or if ``--tmean`` or
``--tstddev`` are explicitly specified (defaults are mean of 50,
standard deviation of 10).

You may recall from your statistics class that a z-score is simply the
value normalized by mean and standard deviation, so that 0.0 is the mean
and positive or negative values are multiples of the standard deviation.
It assumes data follows a normal (Gaussian) distribution.

T-score scales the z-score to match a mean of 50 and a standard
deviation of 10. This program allows generalized t-scores that use any
mean and standard deviation.

Other scales are sometimes used as well. The Wechsler Adult Intelligence
Scale (one type of IQ test) is adjusted to a mean of 100 and a standard
deviation of 15. Other tests scale to other standard deviations.

This program requires two passes over the data, and consumes O(1) memory
and O(number of rows) disk space.

OPTIONS
-------

-a or --include-non-numeric
   Compute stats over all records (treat non-numeric records as zero
   rather than just ignoring them).

-t
   Compute t-scores in addition to z-scores.

--tmean MEAN
   Use the given MEAN for t-scores.

--tstddev STDDEV or --tsd STDDEV
   Use the given STDDEV for the standard deviation of the t-scores.

-f FORMAT or --format FORMAT
   Specify a **printf** (3)-style format for output statistics. Defaults
   to ``%.5g``.

-T TmpDir
   where to put tmp files. Also uses environment variable TMPDIR, if -T
   is not specified. Default is /tmp.

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

cat DATA/grades.fsdb \| dbcolstatscores --tmean 50 --tstddev 10 test1 \|
dbcolneaten

Output:
-------

#fsdb name id test1 zscore:d tscore:d a 1 80 0.23063 52.306 b 2 70
-0.69188 43.081 c 3 65 -1.1531 38.469 d 4 90 1.1531 61.531 e 5 70
-0.69188 43.081 f 6 90 1.1531 61.531 # \| dbcolstatscores --tmean 50
--tstddev 10 test1 # \| dbcolneaten

SEE ALSO
--------

**dbcolpercentile** (1), **dbcolstats** (1), Fsdb, dbcolscorrelate

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
