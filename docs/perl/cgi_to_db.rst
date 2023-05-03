cgi_to_db - convert stored CGI files (from CGI.pm) to fsdb
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

cgi_to_db [-duU] [-e EmptyValue] [cgi-files...]

DESCRIPTION
-----------

Converts all stored CGI files (from CGI.pm) to fsdb, optionally
unescaping the contents. When contents are unescaped, CR NL is recoded
as \``\n''.

Output is always in fsdb list format with double space (type \``S'')
field separator.

Unlike most Fsdb programs, the input to this program is *not* usually
from standard input. However, the program will take ``-i`` options.

This program requires temporary storage equal to the size of the data
(so that it can handle the case of different entries having different
headers).

OPTIONS
-------

-u or --unescape
   do unescape data, converting CGI escape codes like ``%xx`` to regular
   characters (default)

-U or --nounescape
   do *not* unescape data, but leave it CGI-encoded

-e E or --empty E
   give value E as the value for empty (null) records

-T TmpDir
   where to put tmp files. Also uses environment variable TMPDIR, if -T
   is not specified. Default is /tmp.

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

file A (TEST/cgi_to_db_ex.in):

name=test id=111-11-1111 email=test%40usc.edu
submit_time=Tue%20Jan%2014%2011%3A32%3A39%202003 =

file B (TEST/cgi_to_db_ex.in-2):

name=test2 id=222-22-2222 email=test2%40usc.edu newfield=foo emptyfield=
submit_time=Tue%20Jan%2024%2022%3A32%3A39%202003 =

Command:
--------

cgi_to_db TEST/cgi_to_db_ex.in TEST/cgi_to_db_ex.in-2

Output:
-------

#fsdb -R C -F S name id email submit_time newfield emptyfield name: test
id: 111-11-1111 email: test\@usc.edu submit_time: Tue Jan 14 11:32:39
2003 name: test2 id: 222-22-2222 email: test2\@usc.edu newfield: foo
emptyfield: - submit_time: Tue Jan 24 22:32:39 2003 # \| cgi_to_db
TEST/cgi_to_db_ex.in TEST/cgi_to_db_ex.in-2

SEE ALSO
--------

Fsdb. **CGI** (3pm). <http://stein.cshl.org/boulder/>.
<http://stein.cshl.org/WWW/software/CGI/>

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
