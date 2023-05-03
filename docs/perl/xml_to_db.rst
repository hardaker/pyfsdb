xml_to_db - convert a subset of XML into fsdb
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

xml_to_db -k EntityField <source.xml

DESCRIPTION
-----------

Converts a *very limited* subset of XML into Fsdb format.

The input is XML-format (*not* fsdb). The input is parsed as XML, and
each entity of type ENTITYFIELD is extracted as a row. ENTITYFIELD can
have mutliple components separated by slashes to walk down the XML tree,
if necessary.

The input XML file is assumed to be *very simple*. All rows are assumed
to be sequential in one entity. Any other than the specified ENTITYFIELD
are ignored. The schema is assumed to be defined by the first instances
of that field.

The output is two-space-separated fsdb. (Someday more general field
separators should be supported.) Fsdb fields are normalized version of
the CSV file: spaces are converted to single underscores.

OPTIONS
-------

-e EmptyValue or --empty
   Specify the value newly created columns get.

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

<?xml version=1.0 standalone=yes?> <gnuPod> <files> <file
addtime="3389919728" album="Born to Pick" artist="7th Day Buskers"
title="Loch Lamor" /> <file addtime="3389919728" album="Born to Pick"
artist="7th Day Buskers" title="The Floods" /> <file
addtime="3389919735" album="Copland Conducts Copland" artist="Aaron
Copland" title="Our Town" /> </files> <playlist name="new shows"
plid="97241" > <regex artist="^(Le Show|This American Life)$" />
</playlist> </gnuPod>

Command:
--------

xml_to_db -k files/file <gnupod.xml

Output:
-------

#fsdb -F S addtime album artist title 3389919728 Born to Pick 7th Day
Buskers Loch Lamor 3389919728 Born to Pick 7th Day Buskers The Floods
3389919735 Copland Conducts Copland Aaron Copland Our Town # \|
xml_to_db -k files/file

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2011-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
