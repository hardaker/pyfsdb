db_to_html_table - convert db to an HTML table
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

db_to_html_table [-g N] <source.fsdb >dest.html

DESCRIPTION
-----------

Covert an existing dbtable to an HTML table. The output is a fragment of
an HTML page; we assume the user fills in the rest (head and body,
etc.).

Input is fsdb format.

Output is HTML code (*not* fsdb), with HTML-specific characters (less
than, greater than, ampersand) are escaped. (The fsdb-1.x version
assumed input was ISO-8859-1; we now assume both input and output are
unicode. This change is considered a feature of the 21st century.)

OPTIONS
-------

-g N or <--group-count N>
   Color groups of *N* consecutive rows with one background color.

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

#fsdb -F S account passwd uid gid fullname homedir shell johnh \* 2274
134 John & Ampersand /home/johnh /bin/bash greg \* 2275 134 Greg <
Lessthan /home/greg /bin/bash root \* 0 0 Root ; Semi /root /bin/bash
four \* 1 1 Fourth Row /home/four /bin/bash

Command:
--------

cat data.fsdb \| db_to_csv -g 3

Output:
-------

<table> <tr><th>account</th> <th>passwd</th> <th>uid</th> <th>gid</th>
<th>fullname</th> <th>homedir</th> <th>shell</th> </tr> <tr
bgcolor="#f0f0f0"><td>johnh</td> <td>*</td> <td>2274</td> <td>134</td>
<td>John &amp; Ampersand</td> <td>/home/johnh</td> <td>/bin/bash</td>
</tr> <tr bgcolor="#f0f0f0"><td>greg</td> <td>*</td> <td>2275</td>
<td>134</td> <td>Greg &lt; Lessthan</td> <td>/home/greg</td>
<td>/bin/bash</td> </tr> <tr bgcolor="#f0f0f0"><td>root</td> <td>*</td>
<td>0</td> <td>0</td> <td>Root ; Semi</td> <td>/root</td>
<td>/bin/bash</td> </tr> <tr bgcolor="#d0d0d0"><td>four</td> <td>*</td>
<td>1</td> <td>1</td> <td>Fourth Row</td> <td>/home/four</td>
<td>/bin/bash</td> </tr> </table>

SEE ALSO
--------

Fsdb. dbcolneaten. dbfileadjust. html_table_to_db.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2007-2015 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
