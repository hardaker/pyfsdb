dbcolmerge - merge multiple columns into one
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolmerge [-C ElementSeparator] [columns...]

DESCRIPTION
-----------

For each row, merge multiple columns down to a single column (always a
string), joining elements with ElementSeparator (defaults to a single
underscore).

OPTIONS
-------

-C S or --element-separator S
   Specify the separator used to join columns. (Defaults to a single
   underscore.)

-e E or --empty E
   give value E as the value for empty (null) records

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

#fsdb first last John Heidemann Greg Johnson Root - # this is a simple
database # \| /home/johnh/BIN/DB/dbcol fullname # \| dbcolrename
fullname first_last # \| /home/johnh/BIN/DB/dbcolsplit -C \_ first_last
# \| /home/johnh/BIN/DB/dbcol first last

Command:
--------

cat data.fsdb \| dbcolmerge -C \_ first last

Output:
-------

#fsdb first last first_last John Heidemann John_Heidemann Greg Johnson
Greg_Johnson Root - Root\_ # this is a simple database # \|
/home/johnh/BIN/DB/dbcol fullname # \| dbcolrename fullname first_last #
\| /home/johnh/BIN/DB/dbcolsplit first_last # \|
/home/johnh/BIN/DB/dbcol first last # \| /home/johnh/BIN/DB/dbcolmerge
-C \_ first last

SEE ALSO
--------

Fsdb. dbcolsplittocols. dbcolsplittorows. dbcolrename.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
