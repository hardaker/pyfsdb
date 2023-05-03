dbjoin - join two tables on common columns
======================================================================

*NOTE: this page was directly converted from the perl manual page*

SYNOPSIS
--------

dbjoin [-Sid] --input table1.fsdb --input table2.fsdb [-nNrR] column
[column...]

OR

cat table1.fsdb \| dbjoin [-Sid] --input table2.fsdb [-nNrR] column
[column...]

DESCRIPTION
-----------

Does a natural, inner join on TABLE1 and TABLE2 the specified columns.
With the ``-a`` option, or with ``-t outer`` it will do a natural, full
outer join.

(Database review: inner joints output records only when there are
matches in both tables and will omit records that do not match. Outer
joins output all records from both tables, filling with the empty value
as needed. Right (left) outer joins keep all elements of the right
(left) table, even those that don't match in the other table.)

By default for non-hash joins, data will be sorted lexically, but the
usual sorting options can be mixed with the column specification.

Because two tables are required, input is typically in files. Standard
input is accessible by the file -.

If only one input is given, the first (left) input is taken from stdin.

RESOURCE REQUIREMENTS AND PERFORMANCE
-------------------------------------

Joins can be expensive. Most databases have a query optimizer that knows
something about the data and so can select algorithms for efficent
operation, in Fsdb, *you* are that optimizer.

For *non-hash joins*: If data is already sorted, dbjoin will run more
efficiently by telling dbjoin the data is sorted with the ``-S``.

The resource requirements dbjoin vary. If input data is sorted and
``-S`` is given, then memory consumption is bounded by the the sum of
the largest number of records in either dataset with the same value in
the join column, and there is no disk consumption. If data is not
sorted, then dbjoin requires disk storage the size of both input files.

One can minimize memory consumption by making sure each record of table1
matches relatively few records in table2. Typically this means that
table2 should be the smaller. For example, given two files: people.fsdb
(schema: name iso_country_code) and countries.fsdb (schema:
iso_country_code full_country_name), then

dbjoin -i people.fsdb -i countries.fsdb iso_country_code

will require less memory than

dbjoin -i countries.fsdb -i people.fsdb iso_country_code

if there are many people per country (as one would expect). If warning
lots of matching rows accumulating in memory appears, this is the cause
and try swapping join order.

For *hash joins* (that is, with ``-m righthash`` or ``-m lefthash``):
all of the right table (the second input) or the left (the first) is
loaded into memory (and hashed). The other table need not be sorted.
Runtime is O(n), but memory is O(size of hashed table).

OPTIONS
-------

-a or --all
   Perform a *full outer join*, include non-matches (each record which
   doesn't match at all will appear once). Default is an *inner join*.

-t TYPE or --type TYPE
   Explicitly specify the join type. TYPE must be inner, outer, left
   (outer), right (outer). (Recall tha inner join requires data on both
   sides, outer joins keep all records from both sides for outer, or all
   of the first or second input for left and right outer joins.)
   Default: inner.

-m METHOD or --method METHOD
   Select join method (algorithm). Choices are merge, righthash, and
   lefthash. Default: merge.

-S or --pre-sorted
   assume (and verify) data is already sorted

-e E or --empty E
   give value E as the value for empty (null) records

-T TmpDir
   where to put tmp files. Also uses environment variable TMPDIR, if -T
   is not specified. Default is /tmp.

Sort specification options (can be interspersed with column names):

-r or --descending
   sort in reverse order (high to low)

-R or --ascending
   sort in normal order (low to high)

-n or --numeric
   sort numerically

-N or --lexical
   sort lexicographically

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

#fsdb sid cid 1 10 2 11 1 12 2 12

And in the file *DATA/classes*:

#fsdb cid cname 10 pascal 11 numanal 12 os

Command:
--------

cat DATA/reg.fsdb \| dbsort -n cid \| dbjoin -i - -i DATA/classes -n cid

Output:
-------

#fsdb cid sid cname 10 1 pascal 11 2 numanal 12 1 os 12 2 os # -
COMMENTS: # \| /home/johnh/BIN/DB/dbsort -n cid # DATA/classes COMMENTS:
# joined comments: # \| /home/johnh/BIN/DB/dbjoin - DATA/classes cid

SEE ALSO
--------

Fsdb.

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
