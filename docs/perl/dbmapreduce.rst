dbmapreduce - reduce all input rows with the same key
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbmapreduce [-dMS] [-k KeyField] [-f CodeFile] [-C Filtercode] [--]
[ReduceCommand [ReduceArguments...]]

DESCRIPTION
-----------

Group input data by KeyField, then apply a function (the reducer) to
each group. The reduce function can be an external program given by
ReduceCommand and ReduceArguments, or an Perl subroutine given in
CodeFile or FilterCode.

If a -- appears before reduce command, arguments after the Ω- passed the
the command.

Grouping (The Mapper)
---------------------

By default the KeyField is the first field in the row. Unlike Hadoop
streaming, the -k KeyField option can explicitly name where the key is
in any column of each input row.

By default, we sort the data to make sure data is grouped by key. If the
input is already grouped, the ``-S`` option avoids this cost.

The Reducer
-----------

Reduce functions default to be shell commands. However, with ``-C``, one
can use arbitrary Perl code

(see the ``-C`` option below for details). the ``-f`` option is useful
to specify complex Perl code somewhere other than the command line.

Finally, as a special case, if there are no rows of input, the reducer
will be invoked once with the empty value (if it's an external reducer)
or with undef (if it's a subroutine). It is expected to generate the
output header, and it may generate no data rows itself, or a null data
row of its choosing.

Output
------

For non-multi-key-aware reducers, we add the KeyField use for each
Reduce is in the output stream. (If the reducer passes the key we trust
that it gives a correct value.) We also insure that the output field
separator is the same as the input field separator.

Adding the key and adjusting the output field separator is not possible
for non-multi-key-aware reducers.

Comparison to Related Work
--------------------------

This program thus implements Google-style map/reduce, but executed
sequentially.

For input, these systems include a map function and apply it to input
data to generate the key. We assume this key generation (the map
function) has occurred head of time.

We also allow the grouping key to be in any column. Hadoop Streaming
requires it to be in the first column.

By default, the reducer gets exactly (and only) one key. This invariant
is stronger than Google and Hadoop. They both pass multiple keys to the
reducer, insuring that each key is grouped together. With the ``-M``
option, we also pass multiple multiple groups to the reducer.

Unlike those systems, with the ``-S`` option we do not require the
groups arrive in any particular order, just that they be grouped
together. (They guarantees they arrive in lexically sorted order).
However, with ``-S`` we create lexical ordering.

With ``--prepend-key`` we insure that the KeyField is in the output
stream; other systems do not enforce this.

Assumptions and requirements
----------------------------

By default, data can be provided in arbitrary order and the program
consumes O(number of unique tags) memory, and O(size of data) disk
space.

With the ``-S`` option, data must arrive group by tags (not necessarily
sorted), and the program consumes O(number of tags) memory and no disk
space. The program will check and abort if this precondition is not met.

With two ``-S``'s, program consumes O(1) memory, but doesn't verify that
the data-arrival precondition is met.

The field separators of the input and the output can now be different
(early versions of this tool prohibited such variation.) With
``--copy-fs`` we copy the input field separator to the output, but only
for non-multi-key-aware reducers. (this used to be done automatically).
Alternatively, one can specify the output field separator with
``--fieldseparator``, in which case the output had better generate that
format. An explicit ``--fieldseparator`` takes priority over
``--copy-fs``.

Known bugs
----------

As of 2013-09-21, we don't verify key order with options ``-M -S``.

OPTIONS
-------

-k or --key KeyField
   Specify which column is the key for grouping (default: the first
   column). Note that dbmapreduce can only operate on one column as the
   key. To group on the combination of multiple columns, one must merge
   them, perhaps with dbcolmerge.

-S or --pre-sorted
   Assume data is already grouped by tag. Provided twice, it removes the
   validation of this assertion.

-M or --multiple-ok
   Assume the ReduceCommand can handle multiple grouped keys, and the
   ReduceCommand is responsible for outputting the with each output row.
   (By default, a separate ReduceCommand is run for each key, and
   dbmapreduce adds the key to each output row.)

-K or --pass-current-key
   Pass the current key as an argument to the external, non-map-aware
   ReduceCommand. This is only done optionally since some external
   commands do not expect an extra argument. (Internal, non-map-aware
   Perl reducers are always given the current key as an argument.)

--prepend-key
   Add the current key into the reducer output for non-multi-key-aware
   reducers only. Not done by default.

--copy-fs or --copy-fieldseparator
   Change the field separator of a non-multi-key-aware reducers to match
   the input's field separator. Not done by default.

--parallelism=N or -j N
   Allow up to N reducers to run in parallel. Default is the number of
   CPUs in the machine.

-F or --fs or --fieldseparator S
   Specify the field (column) separator as ``S``. See dbfilealter for
   valid field separators.

-C FILTER-CODE or --filter-code=FILTER-CODE
   Provide FILTER-CODE, Perl code that generates and returns a
   Fsdb::Filter object that implements the reduce function. The provided
   code should be an anonymous sub that creates a Fsdb Filter that
   implements the reduce object. The reduce object will then be called
   with --input and --output parameters that hook it into a the reduce
   with queues. One sample fragment that works is just:
   dbcolstats(qw(--nolog duration)) So this command: cat DATA/stats.fsdb
   \| \\ dbmapreduce -k experiment -C dbcolstats(qw(--nolog duration))
   is the same as the example cat DATA/stats.fsdb \| \\ dbmapreduce -k
   experiment -- dbcolstats duration except that with ``-C`` there is no
   forking and so things run faster. If ``dbmapreduce`` is invoked from
   within Perl, then one can use a code SUB as well: dbmapreduce(-k =>
   'experiment', -C => sub { dbcolstats(qw(--nolong duration)) }); The
   reduce object must consume *all* input as a Fsdb stream, and close
   the output Fsdb stream. (If this assumption is not met the map/reduce
   will be aborted.) For non-map-reduce-aware filters, when the
   filter-generator code runs, ``$_[0]`` will be the current key.

-f CODE-FILE or --code-file=CODE-FILE
   Includes *CODE-FILE* in the program. This option is useful for more
   complicated perl reducer functions. Thus, if reducer.pl has the code.
   sub make_reducer { my($current_key) = @_; dbcolstats(qw(--nolog
   duration)); } Then the command cat DATA/stats.fsdb \| \\ dbmapreduce
   -k experiment -f reducer.pl -C make_reducer does the same thing as
   the example.

-w or --warnings
   Enable warnings in user supplied code. Warnings are issued if an
   external reducer fails to consume all input. (Default to include
   warnings.)

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

--header H
   Use H as the full Fsdb header, rather than reading a header from then
   input.

--help
   Show help.

--man
   Show full manual.

SAMPLE USAGE
------------

Input:
------

#fsdb experiment duration ufs_mab_sys 37.2 ufs_mab_sys 37.3 ufs_rcp_real
264.5 ufs_rcp_real 277.9

Command:
--------

cat DATA/stats.fsdb \| \\ dbmapreduce --prepend-key -k experiment --
dbcolstats duration

Output:
-------

#fsdb experiment mean stddev pct_rsd conf_range conf_low conf_high
conf_pct sum sum_squared min max n ufs_mab_sys 37.25 0.070711 0.18983
0.6353 36.615 37.885 0.95 74.5 2775.1 37.2 37.3 2 ufs_rcp_real 271.2
9.4752 3.4938 85.13 186.07 356.33 0.95 542.4 1.4719e+05 264.5 277.9 2 #
\| dbmapreduce -k experiment dbstats duration

SEE ALSO
--------

Fsdb. dbmultistats dbrowsplituniq

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
