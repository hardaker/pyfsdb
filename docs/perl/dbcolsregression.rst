dbcolsregression - compute linear regression between two columns
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolsregression [-a] column1 column2

DESCRIPTION
-----------

Compute linear regression over ``column1`` and ``column2``. Outputs
slope, intercept, and correlation coefficient.

OPTIONS
-------

-a or --include-non-numeric
   Compute stats over all records (treat non-numeric records as zero
   rather than just ignoring them).

-f FORMAT or --format FORMAT
   Specify a **printf** (3)-style format for output statistics. Defaults
   to ``%.5g``.

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

#fsdb x y 160 126 180 103 200 82 220 75 240 82 260 40 280 20

Command:
--------

cat DATA/xy.fsdb \| dbcolsregression x y \| dblistize

Output:
-------

#fsdb -R C slope:d intercept:d confcoeff:d n:q slope: -0.79286
intercept: 249.86 confcoeff: -0.95426 n: 7 # \| dbcolsregression x y #
confidence intervals assume normal distribution and small n. # \|
dblistize

Sample data from
<http://people.hofstra.edu/faculty/Stefan_Waner/RealWorld/calctopic1/regression.html>
by Stefan Waner and Steven R. Costenoble.

SEE ALSO
--------

dbcolstats, dbcolscorrelate, Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1997-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
