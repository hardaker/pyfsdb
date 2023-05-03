dbfilepivot - pivot a table, converting multiple rows into single wide
======================================================================


*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbfilepivot [-e empty] -k KeyField -p PivotField [-v ValueField]

DESCRIPTION
-----------

Pivot a table, converting multiple rows corresponding to the same key
into a single wide row.

In a normalized database, one might have data with a schema like (id,
attribute, value), but sometimes it's more convenient to see the data
with a schema like (id, attribute1, attribute2). (For example, gnuplot's
stacked histograms requires denormalized data.) Dbfilepivot converts the
normalized format to the denormalized, but sometimes useful, format.
Here the id is the key, the attribute is the pivot, and the value is,
well, the optional value.

An example is clearer. A gradebook usually looks like:

#fsdb name hw_1 hw_2 hw_3 John 97 98 99 Paul - 80 82

but a properly normalized format would represent it as:

#fsdb name hw score John 1 97 John 2 98 John 3 99 Paul 2 80 Paul 3 82

This tool converts the second form into the first, when used as

dbfilepivot -k name -p hw -v score

or

dbfilepivot --possible-pivots=1 2 3 -k name -p hw -v score

Here name is the *key* column that indicates which rows belong to the
same entity, hw is the *pivot* column that will be indicate which column
in the output is relevant, and score is the *value* that indicates what
goes in the output.

The pivot creates a new column ``key_tag1``, ``key_tag2``, etc. for each
tag, the contents of the pivot field in the input. It then populates
those new columns with the contents of the value field in the input.

If no value column is specified, then values are either empty or 1.

Dbfilepivot assumes all lines with the same key are adjacent in the
input source, like **dbmapreduce** (1) with the *-S* option. To enforce
this invariant, by default, it *requires* input be sorted by key.

There is no requirement that the pivot field be sorted (provided the key
field is already sorted).

By default, dbfilepivot makes two passes over its data and so requires
temporary disk space equal to the input size. With the
**--possible-pivots** option, the user can specify pivots and skip the
second pass and avoid temporary data storage.

Memory usage is proportional to the number of unique pivot values.

The inverse of this commend is dbcolsplittorows.

OPTIONS
-------

-k or --key KeyField
   specify which column is the key for grouping. Required (no default).

-p or --pivot PivotField
   specify which column is the key to indicate which column in the
   output is relevant. Required (no default).

-v or --value ValueField
   Specify which column is the value in the output. If none is given, 1
   is used for the value.

--possible-pivots PP
   Specify all possible pivot values as PP, a whitespace-separated list.
   With this option, data is processed only once (not twice).

-C S or --element-separator S
   Specify the separator *S* used to join the input's key column with
   its contents. (Defaults to a single underscore.)

-e E or --empty E
   give value E as the value for empty (null) records

-S or --pre-sorted
   Assume data is already grouped by key. Provided twice, it removes the
   validation of this assertion. By default, we sort by key.

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

#fsdb name hw score John 1 97 John 2 98 John 3 99 Paul 2 80 Paul 3 82

Command:
--------

cat data.fsdb \| dbfilepivot -k name -p hw -v score

Output:
-------

#fsdb name hw_1 hw_2 hw_3 John 97 98 99 Paul - 80 82 # \| dbfilepivot -k
name -p hw -v score

SEE ALSO
--------

**Fsdb** (3). **dbcolmerge** (1). **dbcolsplittorows** (1).
**dbcolsplittocols** (1).

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 2011-2022 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
