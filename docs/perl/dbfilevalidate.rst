dbfilevalidate - insure the source input is a well-formed Fsdb file
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbfilevalidate [-vc]

DESCRIPTION
-----------

Validates the input file to make sure it is a well-formed fsdb file. If
the file is well-formed, it outputs the whole file and exits with a good
exit code. For invalid files, it exits with an error exit code and
embedded error messages in the stream as comments with \**\* in them.

Currently this program checks for rows with missing or extra columns.

OPTIONS
-------

-v or --errors-only
   Output only broken lines, not the whole thing.

-c or --correct
   Correct errors, if possible. Pad out rows with the empty value;
   truncate rows with extra values. If errors can be corrected the
   program exits with a good return code.

"-e E" or "--empty E"
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

--help
   Show help.

--man
   Show full manual.

SAMPLE USAGE
------------

Input:
------

#fsdb sid cid 1 10 2 1 12 2 12

Command:
--------

cat TEST/dbfilevalidate_ex.in \| dbvalidate

Output:
-------

#fsdb sid cid 1 10 2 # \**\* line above is missing field cid. 1 12 2 12
# \| dbfilevalidate

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2008 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
