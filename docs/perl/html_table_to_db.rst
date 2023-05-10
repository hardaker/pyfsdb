html_table_to_db - convert HTML tables into fsdb
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

html_table_to_db <source.html >dest.fsdb

DESCRIPTION
-----------

Converts a HTML table to Fsdb format.

The input is an HTML table (*not* fsdb). Column names are taken from
``TH`` elements, or defined as ``column0`` through ``columnN`` if no
such elements appear.

The output is two-space-separated fsdb. (Someday more general field
separators should be supported.) Fsdb fields are normalized version of
the html file: multiple spaces are compressed to one.

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

Command:
--------

html_table_to_db

Output:
-------

#fsdb -F S account passwd uid gid fullname homedir shell johnh \* 2274
134 John & Ampersand /home/johnh /bin/bash greg \* 2275 134 Greg <
Lessthan /home/greg /bin/bash root \* 0 0 Root ; Semi /root /bin/bash
four \* 1 1 Fourth Row /home/four /bin/bash

SEE ALSO
--------

Fsdb. db_to_html_table.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2015 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
