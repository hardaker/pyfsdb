dbcolsplittocols - split an existing column into multiple new columns
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolsplittocols [-E] [-C ElementSeparator] column

DESCRIPTION
-----------

Create new columns by splitting an existing column. The fragments of the
column are each divided by ElementSeparator (default is underscore).

This command is the opposite of dbcolmerge. Names of the new columns are
given by splitting the name of the existing column. dbcolrename may be
useful to set column names.

Input treated as strings and output columns are of type string.

OPTIONS
-------

-C S or --element-separator S
   Specify the separator *S* used to join columns. Usually a signle
   character, it can also be a regular expression (so, for example, [,_]
   matches either , or \_ as an element separator.) (Defaults to a
   single underscore.)

-E or --enumerate
   Enumerate output columns: rather than assuming the column name uses
   the element separator, we keep it whole and fill in with indexes
   starting from 0. (Not currently implemented, but planned. See
   dbcolsplittorows.)

-N on --new-name
   Specify the names of the new columns as a *space* separated list.
   (Default is to apply the separator to the name of the column that is
   being split.) By default, column ``a_b`` will split to columns a and
   b. If the column is given as ab with option ``-N a b``, one will get
   the same result.

-E or --enumerate
   Enumerate output columns: rather than assuming the column name uses
   the element separator, we keep it whole and fill in with indexes
   starting from 0. (Not currently implemented, but planned. See
   dbcolsplittorows.)

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

#fsdb first_last John_Heidemann Greg_Johnson Root # this is a simple
database # \| dbcolrename fullname first_last # \|
/home/johnh/BIN/DB/dbcol first_last

Command:
--------

cat data.fsdb \| dbcolsplittocols first_last

Output:
-------

#fsdb first_last first last John_Heidemann John Heidemann Greg_Johnson
Greg Johnson Root Root # this is a simple database # \| dbcolrename
fullname first_last # \| /home/johnh/BIN/DB/dbcol first_last # \|
/home/johnh/BIN/DB/dbcolsplittocols first_last

SEE ALSO
--------

**Fsdb** (3). **dbcolmerge** (1). **dbcolsplittorows** (1).
**dbcolrename** (1).

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
