dbfilealter - alter the format of an Fsdb file, changing the row/column
======================================================================


*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbfilealter [-c] [-F fs] [-R rs] [-Z compression] [column...]

DESCRIPTION
-----------

This program reformats a Fsdb file, altering the row (``-R rs``) or
column (``-F fs``) separator. It verifies that this action does not
violate the file constraints (for example, if spaces appear in data and
the new format has space as a separator), and optionally corrects
things.

With ``-Z compression`` it controls compression on the file

OPTIONS
-------

-F or --fs or --fieldseparator S
   Specify the field (column) separator as ``S``. See below for valid
   field separators.

-R or --rs or --rowseparator S
   Specify the row separator as ``S``. See below for valid row
   separators.

-Z or --compression S
   Specify file compression as given by file extension ``S``. Supported
   compressions are *gz* for gzip, *bz2* for bzip2, *xz* for xz, or none
   or undef to disable compression. Default is none.

-c or --correct
   Correct any inconsistency caused by the new separators, if possible.

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

Valid Field Separators
----------------------

D default: any amount of whitespace on input, tabs on output.

s single space (exactly one space for input and output).

S double space on output; two or more spaces on input.

t single tab character (exactly one tab for input and output).

XN take N as one or more hex digits that specify a unicode character. Accept one or more of those characters on input, output exactly one of those characters.

CA take A as a one (unicode) literal character. Accept one or more of those characters on input, output exactly one of those characters.

Potentially in the future ``xN`` and ``cA`` will support
single-character-on-input equivalents of ``XN`` and <CA>.

Valid Row Seperators
--------------------

Three row separators are allowed:

D the default, one line per row

C complete rowized. Each line is a field-labeled and its value, and a blank line separates "rows". All fields present in the output.

I incompletely rowized. Like "C", but null fields are omitted from the output.

SAMPLE USAGE
------------

Input:
------

#fsdb name id test1 a 1 80 b 2 70 c 3 65

Command:
--------

cat data.fsdb \| dbfilealter -F S

Output:
-------

#fsdb -F S name id test1 a 1 80 b 2 70 c 3 65 # \| dbfilealter -F S

Command 2:
----------

cat data.fsdb \| dbfilealter -R C

Output:
-------

#fsdb -R C name id test1 name: a id: 1 test1: 80 name: b id: 2 test1: 70
name: c id: 3 test1: 65 # \| dbfilealter -R C

Correction mode input:
----------------------

#fsdb -F S name id test1 a student 1 80 b nice 2 70 c all 3 65

Correction mode command:
------------------------

cat correction.fsdb \| dbfilealter -c -F D

Correction mode output:
-----------------------

#fsdb name id test1 a_student 1 80 b_nice 2 70 c_all 3 65 # \|
dbfilealter -c -F D

SEE ALSO
--------

Fsdb, dbcoldefine.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2008-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
