tabdelim_to_db - convert tab-delimited data into fsdb
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

tabdelim_to_db <source.tabdelim >target.fsdb

DESCRIPTION
-----------

Converts a tab-delimited data stream to Fsdb format.

The input is tab-delimited (*not* fsdb): the first row is taken to be
the names of the columns; tabs separate columns.

The output is a fsdb file with a proper header and a tab
field-separator.

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

name email test1 Tommy Trojan tt@usc.edu 80 Joe Bruin joeb@ucla.edu 85
J. Random jr@caltech.edu 90

Command:
--------

tabdelim_to_db

Output:
-------

#fsdb -Ft name email test1 Tommy Trojan tt@usc.edu 80 Joe Bruin
joeb@ucla.edu 85 J. Random jr@caltech.edu 90 # \| dbcoldefine name email
test1

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2008 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
