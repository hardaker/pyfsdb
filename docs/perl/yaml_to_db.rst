yaml_to_db - convert a subset of YAML into fsdb
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

yaml_to_db <source.yaml

DESCRIPTION
-----------

Converts a *very limited* subset of YAML into Fsdb format.

The input is YAML-format (*not* fsdb). The input is parsed as YAML,
assuming the file is an array of dictionary entries. We extract the
dictionary names and output this as an fsdb table.

The output is tab-separated fsdb. (Someday more general field separators
should be supported.)

OPTIONS
-------

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

- name: ACM role: sponsor alttext: ACM, the Association for Computing
Machinery image: logos/acm-small.jpg link: https://www.acm.org/ date:
2016-01-01 - name: SIGCOMM role: sponsor alttext: SIGCOMM, ACMS Special
Interest Group on Communication image: logos/sigcommlogo.png link:
http://sigcomm.org date: 2016-01-02 - name: SIGMETRICS role: sponsor
alttext: SIGMETRICS, ACMS Special Interest Group on Performance
Evaluation image: logos/sigmetrics-small.png link:
http://www.sigmetrics.org date: 2016-01-03

Command:
--------

yaml_to_db <gnupod.yaml

Output:
-------

#fsdb -F t alttext date image link name role ACM, the Association for
Computing Machinery 2016-01-01 logos/acm-small.jpg https://www.acm.org/
ACM sponsor SIGCOMM, ACMS Special Interest Group on Communication
2016-01-02 logos/sigcommlogo.png http://sigcomm.org SIGCOMM sponsor
SIGMETRICS, ACMS Special Interest Group on Performance Evaluation
2016-01-03 logos/sigmetrics-small.png http://www.sigmetrics.org
SIGMETRICS sponsor # \| yaml_to_db

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2011-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
