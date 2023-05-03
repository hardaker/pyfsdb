kitrace_to_db - convert kitrace output to Fsdb format
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

kitrace_to_db [-Y year] [registers] <kitrace.out >kitrace.fsdb

DESCRIPTION
-----------

Converts a kitrace data stream to Fsdb format.

Optional arguments list registers which will be picked out of the output
stream and formatted as their own columns.

OPTIONS
-------

-Y Y or --year Y
   Specify the 4-digit year for the dataset (defaults to current year).

-u or --utc
   Specify UTC timezone (defaults to local time zeon).

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

\_null_getpage+4 Nov 7 22:40:13.281070 ( ) pid 4893 \_null_getpage+128
Nov 7 22:40:13.281756 ( 00.000686) pid 4893 \_null_getpage+4 Nov 7
22:40:13.282694 ( 00.000938) pid 4893 \_null_getpage+128 Nov 7
22:40:13.328709 ( 00.046015) pid 4893 \_null_getpage+4 Nov 7
22:40:13.330758 ( 00.002049) pid 4893 \_null_getpage+128 Nov 7
22:40:13.353830 ( 00.023072) pid 4893 \_null_getpage+4 Nov 7
22:40:13.355566 ( 00.001736) pid 4893 \_null_getpage+128 Nov 7
22:40:13.357169 ( 00.001603) pid 4893 \_null_getpage+4 Nov 7
22:40:13.358780 ( 00.001611) pid 4893 \_null_getpage+128 Nov 7
22:40:13.375844 ( 00.017064) pid 4893 \_null_getpage+4 Nov 7
22:40:13.377850 ( 00.002006) pid 4893 \_null_getpage+128 Nov 7
22:40:13.378358 ( 00.000508) pid 4893

Command:
--------

kitrace_to_db -Y 1995

Output:
-------

#fsdb event clock diff \_null_getpage+4 815812813.281070 0.0
\_null_getpage+128 815812813.281756 00.000686 \_null_getpage+4
815812813.282694 00.000938 \_null_getpage+128 815812813.328709 00.046015
\_null_getpage+4 815812813.330758 00.002049 \_null_getpage+128
815812813.353830 00.023072 \_null_getpage+4 815812813.355566 00.001736
\_null_getpage+128 815812813.357169 00.001603 \_null_getpage+4
815812813.358780 00.001611 \_null_getpage+128 815812813.375844 00.017064
\_null_getpage+4 815812813.377850 00.002006 \_null_getpage+128
815812813.378358 00.000508 # \| kitrace_to_db

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2011 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
