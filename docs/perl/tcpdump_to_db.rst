tcpdump_to_db - convert tcpdump textual output to fsdb
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

tcpdump_to_db [-T] < source.tcpdump > target.fsdb

DESCRIPTION
-----------

Converts a tcpdump textual data stream to Fsdb format.

**Currently it handles only TCP and silently fails on other traffic!**
Awaiting enhancement... you're welcome to help.

OPTIONS
-------

-t or --daytime
   Adjust times relative to the first timestamp. (Defaults on.)

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

14:11:12.556781 dash.isi.edu.1023 > excalibur.usc.edu.ssh: S
2306448962:2306448962(0) win 32120 <mss 1460,sackOK,timestamp
82802652[|tcp]> (DF) 14:11:12.561734 excalibur.usc.edu.ssh >
dash.isi.edu.1023: S 1968320001:1968320001(0) ack 2306448963 win 4096
14:11:12.561875 dash.isi.edu.1023 > excalibur.usc.edu.ssh: . ack 1 win
32120 (DF) 14:11:18.746567 excalibur.usc.edu.ssh > dash.isi.edu.1023: P
316:328(12) ack 348 win 4096 14:11:18.755176 dash.isi.edu.1023 >
excalibur.usc.edu.ssh: P 348:488(140) ack 328 win 32696 (DF) [tos 0x10]
14:11:18.847937 excalibur.usc.edu.ssh > dash.isi.edu.1023: P
328:468(140) ack 488 win 4096 14:11:18.860047 dash.isi.edu.1023 >
excalibur.usc.edu.ssh: . ack 468 win 32696 (DF) [tos 0x10]
14:11:18.936255 dash.isi.edu.1023 > excalibur.usc.edu.ssh: P 488:516(28)
ack 468 win 32696 (DF) [tos 0x10]

or a more modern form

17:00:14.808855 IP 10.0.0.172.31738 > 10.1.0.50.telnet: Flags [S], seq
3236187954, win 21463, length 0

Command:
--------

tcpdump_to_db

Output:
-------

#fsdb time proto src dest flags start end len ack win 51072.556781 tcp
dash.isi.edu.1023 excalibur.usc.edu.ssh S 2306448962 2306448962 0 -
32120 51072.561734 tcp excalibur.usc.edu.ssh dash.isi.edu.1023 S
1968320001 1968320001 0 2306448963 4096 51072.561875 tcp
dash.isi.edu.1023 excalibur.usc.edu.ssh . - - - 1 32120 51078.746567 tcp
excalibur.usc.edu.ssh dash.isi.edu.1023 P 316 328 12 348 4096
51078.755176 tcp dash.isi.edu.1023 excalibur.usc.edu.ssh P 348 488 140
328 32696 51078.847937 tcp excalibur.usc.edu.ssh dash.isi.edu.1023 P 328
468 140 488 4096 51078.860047 tcp dash.isi.edu.1023
excalibur.usc.edu.ssh . - - - 468 32696 51078.936255 tcp
dash.isi.edu.1023 excalibur.usc.edu.ssh P 488 516 28 468 32696 # \|
tcpdump_to_db

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
