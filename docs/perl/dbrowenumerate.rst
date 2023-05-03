dbrowenumerate - enumerate rows, starting from zero
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbrowenumerate

DESCRIPTION
-----------

Add a new column \``count'', incremented for each row of data, starting
with zero. Use dbrowaccumulate for control over initial value or
increment; this module is just a wrapper around that.

OPTIONS
-------

-N or --new-name N
   Name the new column N. Defaults to ``count``.

This module also supports the standard jdb options:

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

#h account passwd uid gid fullname homedir shell johnh \* 2274 134
John_Heidemann /home/johnh /bin/bash greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash root \* 0 0 Root /root /bin/bash # this is a simple
database

Command:
--------

cat DATA/passwd.jdb \| dbrowenumerate

Output:
-------

#h account passwd uid gid fullname homedir shell count johnh \* 2274 134
John_Heidemann /home/johnh /bin/bash 0 greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash 1 root \* 0 0 Root /root /bin/bash 2 # this is a
simple database # \| /home/johnh/BIN/DB/dbrowenumerate

SEE ALSO
--------

Fsdb, dbrowaccumulate.

CLASS FUNCTIONS
---------------
