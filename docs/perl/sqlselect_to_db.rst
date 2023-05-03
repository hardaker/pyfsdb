sqlselect_to_db - convert MySQL or MariaDB selected tables to fsdb
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

sqlselect_to_db <source.sqlselect_table >dest.fsdb

DESCRIPTION
-----------

Converts a MySQL or MariaDB tables to Fsdb format.

The input is *not* fsdb. The first non-box row is taken to be the names
of the columns.

The output is two-space-separated fsdb. (Someday more general field
separators should be supported.)

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

+----------------+---------------+--------------------+------+-------------------------+
\| username \| firstname \| lastname \| id \| email \|
+----------------+---------------+--------------------+------+-------------------------+
\| johnh \| John \| Heidemann \| 134 \| johnh@isi.edu \|
+----------------+---------------+--------------------+------+-------------------------+
1 row in set (0.01 sec)

Command:
--------

sqlselect_to_db

Output:
-------

#fsdb -F S username firstname lastname id email johnh John Heidemann 134
johnh@isi.edu # \| sqlselect_to_db

SEE ALSO
--------

Fsdb. db_to_csv.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2014-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
