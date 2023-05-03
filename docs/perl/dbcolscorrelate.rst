dbcolscorrelate - find the coefficient of correlation over columns
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolscorrelate column1 column2 [column3...]

DESCRIPTION
-----------

Compute the coefficient of correlation over two (or more) columns.

The output is one line of correlations.

With exactly two columns, a new column *correlation* is created.

With more than two columns, correlations are computed for each pairwise
combination of rows, and each output column is given a name which is the
concatenation of the two source rows, joined with an underscore.

By default, we compute the *population correlation coefficient* (usually
designed rho, X) and assume we see all members of the population. With
the **--sample** option we instead compute the *sample correlation
coefficient*, usually designated *r*. (Be careful in that the default
here to full-population is the *opposite* of the default in dbcolstats.)

This program requires a complete copy of the input data on disk.

OPTIONS
-------

--sample
   Select a the Pearson product-moment correlation coefficient (the
   sample correlation coefficient, usually designated *r*).

--nosample
   Select a the Pearson product-moment correlation coefficient (the
   sample correlation coefficient, usually designated *r*).

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

#fsdb name id test1 test2 a 1 80 81 b 2 70 71 c 3 65 66 d 4 90 91 e 5 70
71 f 6 90 91

Command:
--------

cat DATA/more_grades.fsdb \| dbcolscorrelate test1 test2

Output:
-------

#fsdb correlation:d 0.83329 # \| dbcolscorrelate test1 test2

SEE ALSO
--------

Fsdb, dbcolstatscores, dbcolsregression, dbrvstatdiff.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1998-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
