dbcolrename - change the names of columns in a fsdb schema
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbcolrename OldName1 NewName1 [OldName2 NewName2] ...

DESCRIPTION
-----------

Dbcolrename changes the names of columns in a fsdb schema, mapping
OldName1 to NewName1, and so on for multiple pairs of column names.

Note that it is valid to do overlapping renames like
``dbcolrename a b b a``.

OPTIONS
-------

No non-standard options.

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

#fsdb account passwd uid gid fullname homedir shell johnh \* 2274 134
John_Heidemann /home/johnh /bin/bash greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash root \* 0 0 Root /root /bin/bash # this is a simple
database

Command:
--------

cat DATA/passwd.fsdb \| dbcolrename fullname first_last

Output:
-------

#fsdb account passwd uid gid first_last homedir shell johnh \* 2274 134
John_Heidemann /home/johnh /bin/bash greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash root \* 0 0 Root /root /bin/bash # this is a simple
database # \| dbcolrename fullname first_last

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
