dbfilestripcomments - remove comments from a fsdb file
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbfilestripcomments [-h]

DESCRIPTION
-----------

Remove any comments in a file, including the header. This makes the file
unreadable by other Fsdb utilities, but perhaps more readable by humans.

With the -h option, leave the header.

OPTIONS
-------

-h or --header
   Retain the header.

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

#fsdb -R C experiment mean stddev pct_rsd conf_range conf_low conf_high
conf_pct sum sum_squared min max n experiment: ufs_mab_sys mean: 37.25
stddev: 0.070711 pct_rsd: 0.18983 conf_range: 0.6353 conf_low: 36.615
conf_high: 37.885 conf_pct: 0.95 sum: 74.5 sum_squared: 2775.1 min: 37.2
max: 37.3 n: 2 # \| /home/johnh/BIN/DB/dbmultistats experiment duration
# \| /home/johnh/BIN/DB/dblistize

Command:
--------

cat data.fsdb \| dbfilestripcomments

Output:
-------

experiment: ufs_mab_sys mean: 37.25 stddev: 0.070711 pct_rsd: 0.18983
conf_range: 0.6353 conf_low: 36.615 conf_high: 37.885 conf_pct: 0.95
sum: 74.5 sum_squared: 2775.1 min: 37.2 max: 37.3 n: 2

SEE ALSO
--------

Fsdb. dbcoldefine.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2008 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
