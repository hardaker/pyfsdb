dbrow - select rows from an Fsdb file based on arbitrary conditions
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbrow [-vw] CONDITION [CONDITION...]

DESCRIPTION
-----------

Select rows for which all CONDITIONS are true. Conditions are specified
as Perl code, in which column names are be embedded, preceded by
underscores.

OPTIONS
-------

-v
   Invert the selection, picking rows where at least one condition does
   *not* match.

This module also supports the standard fsdb options:

-d
   Enable debugging output.

-w or --warnings
   Enable warnings in user supplied code.

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

#fsdb account passwd uid gid fullname homedir shell johnh \* 2274 134
John_Heidemann /home/johnh /bin/bash greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash root \* 0 0 Root /root /bin/bash # this is a simple
database

Command:
--------

cat DATA/passwd.fsdb \| dbrow \_fullname =~ /John/

Output:
-------

#fsdb account passwd uid gid fullname homedir shell johnh \* 2274 134
John_Heidemann /home/johnh /bin/bash greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash # this is a simple database # \|
/home/johnh/BIN/DB/dbrow

BUGS
----

Doesn't detect references to unknown columns in conditions.

END #' for font-lock mode. exit 1;

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
