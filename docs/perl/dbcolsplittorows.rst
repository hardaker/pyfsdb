dbcolsplittorows - split an existing column into multiple new rows
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolsplittorows [-C ElementSeperator] [-e null] [-E] [-N
enumerated-name] column [column...]

DESCRIPTION
-----------

Split column into pieces, outputting one row for each piece.

By default, any empty fields are ignored. If an empty field value is
given with -e, then they produce output.

When a null value is given, empty fields at the beginning and end of
lines are suppressed (like perl split). Unlike perl, if ALL fields are
empty, we generate one (and not zero) empty fields.

The inverse of this commend is dbfilepivot.

OPTIONS
-------

-C S or --element-separator S
   Specify the separator used to split columns. (Defaults to a single
   underscore.)

-E or --enumerate
   Enumerate output columns: rather than assuming the column name uses
   the element separator, we keep it whole and fill in with indexes
   starting from 0.

-N or --new-name N
   Name the new column N for enumeration. Defaults to ``index``.

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

--help
   Show help.

--man
   Show full manual.

SAMPLE USAGE
------------

Input:
------

#fsdb name uid John_Heidemann 2274 Greg_Johnson 2275 Root 0 # this is a
simple database # \| dbcol fullname uid # \| dbcolrename fullname name

Command:
--------

cat data.fsdb \| dbcolsplittorows name

Output:
-------

#fsdb name uid John 2274 Heidemann 2274 Greg 2275 Johnson 2275 Root 0 #
this is a simple database # \| dbcol fullname uid # \| dbcolrename
fullname name # \| dbcolsplittorows name

SEE ALSO
--------

**Fsdb** (1). **dbcolmerge** (1). **dbcolsplittocols** (1).
**dbcolrename** (1). **dbfilepvot** (1).

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
