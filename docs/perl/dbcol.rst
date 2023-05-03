dbcol - select columns from an Fsdb file
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbcol [-v] [-e -] [column...]

DESCRIPTION
-----------

Select one or more columns from the input database. If a value is given
for empty columns with the -e option, then any named columns which don't
exist will be created. Otherwise, non-existent columns are an error.

Note: a safer way to create columns is dbcolcreate.

OPTIONS
-------

-r or --relaxed-errors
   Relaxed error checking: ignore columns that aren't there.

-v or --invert-match
   Output all columns except those listed (like grep -v).

-a or --all
   Output all columns, in addition to those listed. (Thus ``-a foo``
   will move column foo to the first column.)

-e EmptyValue or --empty
   Specify the value newly created columns get.

--saveoutput $OUT_REF
   Save output writer (for integration with other fsdb filters).

and the standard fsdb options:

-d
   Enable debugging output.

-i or --input InputSource
   Read from InputSource, typically a file, or - for standard input, or
   (if in Perl) a IO::Handle, Fsdb::IO or Fsdb::BoundedQueue objects.

-o or --output OutputDestination
   Write to OutputDestination, typically a file, or - for standard
   output, or (if in Perl) a IO::Handle, Fsdb::IO or Fsdb::BoundedQueue
   objects.

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

cat DATA/passwd.fsdb account \| dbcol account

Output:
-------

#fsdb account johnh greg root # this is a simple database # \| dbcol
account

SEE ALSO
--------

**dbcolcreate** (1), **Fsdb** (3)

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
