combined_log_format_to_db - convert Apache Combined Log Format to Fsdb
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

combined_log_format_to_db < access_log > access_log.fsdb

DESCRIPTION
-----------

Converts logs in Apache Combined-Log-Format into Fsdb format.

OPTIONS
-------

No program-specific options.

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

foo.example.com - - [01/Jan/2007:00:00:01 -0800] "GET
/~moll/wedding/index.html HTTP/1.0" 200 2390 "-" "Mozilla/5.0
(compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
127.0.0.1 - - [01/Jan/2007:00:00:02 -0800] "GET /hpdc2007/ HTTP/1.1" 304
- "http://grid.hust.edu.cn:8080/call/cfp.jsp" "Mozilla/4.0 (compatible;
MSIE 7.0; Windows NT 5.1; InfoPath.1; InfoPath.2)" bar.example.com - -
[31/Dec/2006:23:51:40 -0800] "GET /nsnam/dist/ns-allinone-2.29.2.tar.gz
HTTP/1.1" 206 58394090
"file://D:\\\xce\xd2\xb5\xc4\xce\xc4\xb5\xb5\\ns2\\XP_Using_Cygwin.htm#Windows_Support_for_Ns-2.27_and_Earlier"
"Mozilla/4.0 (compatible; MSIE 5.00; Windows 98)" 127.0.0.1 - -
[01/Jan/2007:00:00:02 -0800] "GET /hpdc2007/hpdc.css HTTP/1.1" 304 -
"http://www.isi.edu/hpdc2007/" "Mozilla/4.0 (compatible; MSIE 7.0;
Windows NT 5.1; InfoPath.1; InfoPath.2)"

Command:
--------

combined_log_format_to_db

Output:
-------

#fsdb -F S client identity userid time method resource protocol status
size refer useragent foo.example.com - - [01/Jan/2007:00:00:01 -0800]
GET /~moll/wedding/index.html HTTP/1.0 200 2390 "-" "Mozilla/5.0
(compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
127.0.0.1 - - [01/Jan/2007:00:00:02 -0800] GET /hpdc2007/ HTTP/1.1 304 -
"http://grid.hust.edu.cn:8080/call/cfp.jsp" "Mozilla/4.0 (compatible;
MSIE 7.0; Windows NT 5.1; InfoPath.1; InfoPath.2)" bar.example.com - -
[31/Dec/2006:23:51:40 -0800] GET /nsnam/dist/ns-allinone-2.29.2.tar.gz
HTTP/1.1 206 58394090
"file://D:\\\xce\xd2\xb5\xc4\xce\xc4\xb5\xb5\\ns2\\XP_Using_Cygwin.htm#Windows_Support_for_Ns-2.27_and_Earlier"
"Mozilla/4.0 (compatible; MSIE 5.00; Windows 98)" 127.0.0.1 - -
[01/Jan/2007:00:00:02 -0800] GET /hpdc2007/hpdc.css HTTP/1.1 304 -
"http://www.isi.edu/hpdc2007/" "Mozilla/4.0 (compatible; MSIE 7.0;
Windows NT 5.1; InfoPath.1; InfoPath.2)" # \| combined_log_format_to_db

SEE ALSO
--------

Fsdb. <http://httpd.apache.org/docs/2.0/logs.html>

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2008 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
