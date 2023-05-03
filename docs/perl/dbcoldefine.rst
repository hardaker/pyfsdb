dbcoldefine - define the columns of a plain text file to make it an Fsdb
======================================================================


*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbcoldefine [-F x] [column...]

DESCRIPTION
-----------

This program writes a new header before the data with the specified
column names. It does *not* do any validation of the data contents; it
is up to the user to verify that, other than the header, the input
datastream is a correctly formatted Fsdb file.

OPTIONS
-------

-F or --fs or --fieldseparator s
   Specify the field separator.

--header H
   Give the columns and field separator as a full Fsdb header (including
   ``#fsdb``). Can only be used alone, not with other specifications.

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

102400 4937974.964736 102400 4585247.875904 102400 5098141.207123

Command:
--------

cat DATA/http_bandwidth \| dbcoldefine size bw

Output:
-------

#fsdb size bw 102400 4937974.964736 102400 4585247.875904 102400
5098141.207123 # \| dbcoldefine size bw

SEE ALSO
--------

Fsdb. dbfilestripcomments

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2016 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
