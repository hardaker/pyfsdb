dbrvstatdiff - evaluate statistical differences between two random
======================================================================


*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbrvstatdiff [-f format] [-c ConfRating] [-h HypothesizedDifference] m1c
sd1c n1c m2c sd2c n2c

OR

dbrvstatdiff [-f format] [-c ConfRating] m1c n1c m2c n2c

DESCRIPTION
-----------

Produce statistics on the difference of sets of random variables. If a
hypothesized difference is given (with ``-h``), to does a Student's
t-test.

Random variables are specified by:

"m1c", "m2c"
   The column names of means of random variables.

"sd1c", "sd2c"
   The column names of standard deviations of random variables.

"n1c", "n2c"
   Counts of number of samples for each random variable

These values can be computed with dbcolstats.

Creates up to ten new columns:

"diff"
   The difference of RV 2 - RV 1.

"diff_pct"
   The percentage difference (RV2-RV1)/1

"diff_conf_{half,low,high}" and "diff_conf_pct_{half,low,high}"
   The half half confidence intervals and low and high values for
   absolute and relative confidence.

"t_test"
   The T-test value for the given hypothesized difference.

"t_test_result"
   Given the confidence rating, does the test pass? Will be either
   rejected or not-rejected.

"t_test_break"
   The hypothesized value that is break-even point for the T-test.

"t_test_break_pct"
   Break-even point as a percent of m1c.

Confidence intervals are not printed if standard deviations are not
provided. Confidence intervals assume normal distributions with common
variances.

T-tests are only computed if a hypothesized difference is provided.
Hypothesized differences should be proceeded by <=, >=, =. T-tests
assume normal distributions with common variances.

OPTIONS
-------

-c FRACTION or --confidence FRACTION
   Specify FRACTION for the confidence interval. Defaults to 0.95 for a
   95% confidence factor (alpha = 0.05).

-f FORMAT or --format FORMAT
   Specify a **printf** (3)-style format for output statistics. Defaults
   to ``%.5g``.

-h DIFF or --hypothesis DIFF
   Specify the hypothesized difference as ``DIFF``, where ``DIFF`` is
   something like ``<=0`` or ``>=0``, etc.

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

#fsdb title mean2 stddev2 n2 mean1 stddev1 n1 example6.12 0.17 0.0020 5
0.22 0.0010 4

Command:
--------

cat data.fsdb \| dbrvstatdiff mean2 stddev2 n2 mean1 stddev1 n1

Output:
-------

#fsdb title mean2 stddev2 n2 mean1 stddev1 n1 diff:d diff_pct:d
diff_conf_half:d diff_conf_low:d diff_conf_high:d diff_conf_pct_half:d
diff_conf_pct_low:d diff_conf_pct_high:d example6.12 0.17 0.0020 5 0.22
0.0010 4 0.05 29.412 0.0026138 0.047386 0.052614 1.5375 27.874 30.949 #
\| dbrvstatdiff mean2 stddev2 n2 mean1 stddev1 n1

Input 2:
--------

(example 7.10 from Scheaffer and McClave):

#fsdb title x2 sd2 n2 x1 sd1 n1 example7.10 9 35.22 24.44 9 31.56 20.03

Command 2:
----------

dbrvstatdiff -h <=0 x2 sd2 n2 x1 sd1 n1

Output 2:
---------

#fsdb title n1 x1 sd1 n2 x2 sd2 diff diff_pct diff_conf_half
diff_conf_low diff_conf_high diff_conf_pct_half diff_conf_pct_low
diff_conf_pct_high t_test t_test_result example7.10 9 35.22 24.44 9
31.56 20.03 3.66 0.11597 4.7125 -1.0525 8.3725 0.14932 -0.033348 0.26529
1.6465 not-rejected # \|
/global/us/edu/ucla/cs/ficus/users/johnh/BIN/DB/dbrvstatdiff -h <=0 x2
sd2 n2 x1 sd1 n1

Case 3:
-------

A common use case is to have one file with a set of trials from two
experiments, and to use dbrvstatdiff to see if they are different.

*Input 3:*

#fsdb case trial value a 1 1 a 2 1.1 a 3 0.9 a 4 1 a 5 1.1 b 1 2 b 2 2.1
b 3 1.9 b 4 2 b 5 1.9

Command 3:
----------

cat two_trial.fsdb \| dbmultistats -k case value \| dbcolcopylast mean
stddev n \| dbrow \_case eq "b" \| dbrvstatdiff -h =0 mean stddev n
copylast_mean copylast_stddev copylast_n \| dblistize

*Output 3:*

#fsdb -R C case mean stddev pct_rsd conf_range conf_low conf_high
conf_pct sum sum_squared min max n copylast_mean copylast_stddev
copylast_n diff diff_pct diff_conf_half diff_conf_low diff_conf_high
diff_conf_pct_half diff_conf_pct_low diff_conf_pct_high t_test
t_test_result t_test_break t_test_break_pct case: b mean: 1.98 stddev:
0.083666 pct_rsd: 4.2256 conf_range: 0.10387 conf_low: 1.8761 conf_high:
2.0839 conf_pct: 0.95 sum: 9.9 sum_squared: 19.63 min: 1.9 max: 2.1 n: 5
copylast_mean: 1.02 copylast_stddev: 0.083666 copylast_n: 5 diff: -0.96
diff_pct: -48.485 diff_conf_half: 0.12202 diff_conf_low: -1.082
diff_conf_high: -0.83798 diff_conf_pct_half: 6.1627 diff_conf_pct_low:
-54.648 diff_conf_pct_high: -42.322 t_test: -18.142 t_test_result:
rejected t_test_break: -1.082 t_test_break_pct: -54.648 # \|
dbmultistats -k case value # \| dbcolcopylast mean stddev n # \| dbrow
\_case eq "b" # \| dbrvstatdiff -h =0 mean stddev n copylast_mean
copylast_stddev copylast_n # \| dbfilealter -R C

(So one cannot say that they are statistically equal.)

SEE ALSO
--------

Fsdb, dbcolstats, dbcolcopylast, dbcolscorrelate.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2021 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
