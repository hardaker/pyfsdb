dbcolneaten - pretty-print columns of Fsdb data (assuming a monospaced
======================================================================


*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolneaten [-E] [field_settings]

DESCRIPTION
-----------

dbcolneaten arranges that the Fsdb data appears in neat columns if you
view it with a monospaced font. To do this, it pads out each field with
spaces to line up the next field.

Field settings are of the form

field op value

OP is >=, =, or <= specifying that the width of that FIELD must be more,
equal, or less than that VALUE

dbcolneaten runs in O(1) memory but disk space proportional to the size
of data.

OPTIONS
-------

-E or --noeoln
   Omit padding for the last column (at the end-of-the-line). (Default
   behavior.)

-e or --eoln
   Do padding and include an extra field separator after the last
   column. (Useful if you're interactively adding a column.)

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

#fsdb fullname homedir uid gid Mr._John_Heidemann_Junior /home/johnh
2274 134 Greg_Johnson /home/greg 2275 134 Root /root 0 0 # this is a
simple database # \| dbcol fullname homedir uid gid

Command:
--------

dbcolneaten

Output:
-------

#fsdb -F s fullname homedir uid gid Mr._John_Heidemann_Junior
/home/johnh 2274 134 Greg_Johnson /home/greg 2275 134 Root /root 0 0 #
this is a simple database # \| dbcol fullname homedir uid gid # \|
dbcolneaten

BUGS
----

Does not handle tab separators correctly.

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
