dbformmail - write a shell script that will send e-mail to many people
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbformmail [-m MECHANISM] format_file.txt

DESCRIPTION
-----------

Read a \``form mail'' message from the file FORMAT_FILE.TXT, filling in
underscore-preceded column-names with data. Output a shell script which
will send each message through some mail transport MECHANISM.

Do not use this program for evil or I will have to come over and have
words with you.

Note that this program does NOT actually SEND the mail. It writes a
shell script that will send the mail for you. I recommend you save it to
a file, check it (one last time!), then run it with sh.

Unlike most Fsdb programs, this program does *not* output a FSDB file.

OPTIONS
-------

-m MECHANISM
   Select the mail-sending mechanism: Mail, sendmail, mh. Defaults to
   Mail. Mail uses a Berkeley-style /usr/bin/Mail. Sendmail invokes
   /usr/bin/sendmail. Mh writes messages into the current directory,
   treating it as an mh-style mailbox (one message per file, with
   filesnames as sequential integrates).

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

#fsdb account passwd uid gid fullname homedir shell johnh \* 2274 134
John_Heidemann /home/johnh /bin/bash greg \* 2275 134 Greg_Johnson
/home/greg /bin/bash root \* 0 0 Root /root /bin/bash # this is a simple
database

Sample form (in the file form.txt):

To: \_account From: the sysadmin <root> Subject: time to change your
password Please change your password regularly. Doesnt this message make
you feel safer?

Command:
--------

cat DATA/passwd.fsdb \| dbformmail form.txt >outgoing.sh

Output (in outgoing.sh):
------------------------

#!/bin/sh sendmail johnh <<END To: johnh From: the sysadmin <root>
Subject: time to change your password Please change your password
regularly. Doesnt this message make you feel safer? END sendmail greg
<<END (etc.)

And to send the mail, run

sh outgoing.sh

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
