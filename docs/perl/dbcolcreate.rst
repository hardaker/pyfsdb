dbcolcreate - create new columns
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbcolcreate NewColumn1 [NewColumn2]

or

dbcolcreate -e DefaultValue NewColumnWithDefault

DESCRIPTION
-----------

Create columns ``NewColumn1``, etc. with an optional ``DefaultValue``.

OPTIONS
-------

-e EmptyValue or --empty
   Specify the value newly created columns get.

-f or --first
   Put all new columns as the first columns of each row. By default,
   they go at the end of each row.

--no-recreate-fatal
   By default, creating an existing column is an error. With
   **--no-recreate-fatal**, we ignore re-creation.

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

#fsdb test a b

Command:
--------

cat data.fsdb \| dbcolcreate foo

Output:
-------

#fsdb test foo a - b -

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
