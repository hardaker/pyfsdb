dbcoltype - define (or redefine) types for columns of an Fsdb file
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbcol [-v] [column type...]

DESCRIPTION
-----------

Define the type of each column, where COLUMN and TYPE are pairs. Or,
with the ``-v`` option, redefine all types as string.

The data does not change (just the header).

OPTIONS
-------

-v or --clear-types
   Remove definitions from columns that are listed, or from all columns
   if none are listed. The effect is to restore types to their default
   type of a (string).

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

cat DATA/passwd.fsdb account \| dbcoltype uid l gid l

Output:
-------

#fsdb account passwd uid:l gid:l fullname homedir shell johnh \* 2274
134 John_Heidemann /home/johnh /bin/bash greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash root \* 0 0 Root /root /bin/bash # this is a simple
database

SEE ALSO
--------

**dbcoldefine** (1), **dbcolcreate** (1), **Fsdb** (3).

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
