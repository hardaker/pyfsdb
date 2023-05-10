dbroweval - evaluate code for each row of a fsdb file
======================================================================

*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version 3.1*

SYNOPSIS
--------

dbroweval [-f CodeFile] code [code...]

DESCRIPTION
-----------

Evaluate code for each row of the data.

Typical actions are things like reformatting and other data
transformations.

Code can include embedded column names preceded by underscores; these
result in the value of that column for the current row.

The values of the last row's columns are retrieved with \_last_foo where
foo is the column name.

Even more perverse, \_columname(N) is the value of the Nth column after
columnname [so **\_columnname** (0) is the also the column's value.

OPTIONS
-------

-b CODE
   Run CODE before reading any data (like awk BEGIN blocks).

-e CODE
   Run CODE at the end of all data (like awk END blocks).

-f FILE
   Read code from the FILE.

-n or --no-output
   no output except for comments and what is in the provided code

-N or --no-output-even-comments
   no output at all, except for what is in the provided code

-m or --manual-output
   The user must setup output, allowing arbitrary comments. See example
   2 below for details.

-w or --warnings
   Enable warnings in user supplied code.

--saveoutput $OUT_REF
   Save output writer (for integration with other fsdb filters).

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

ADVANCED USAGE
--------------

Typically dbroweval outputs a line in the same schema for each input
line. For advanced usage, one can violate each of these assumptions.

Some fun:

omitting a line
   Add the code ``next row if ($your condition);``

outputting an extra line
   Call ``&$write_fastpath_sub($fref)``. You may find ``$fref``, the
   input row, useful.

changing the schema
   See the examples below in Command 2: Changing the Schema

SAMPLE USAGE
------------

Input:
------

#fsdb size mean stddev pct_rsd 1024 1.4962e+06 2.8497e+05 19.047 10240
5.0286e+06 6.0103e+05 11.952 102400 4.9216e+06 3.0939e+05 6.2863 # \|
dbsetheader size bw # \| /home/johnh/BIN/DB/dbmultistats size bw # \|
/home/johnh/BIN/DB/dbcol size mean stddev pct_rsd

Command:
--------

cat data.fsdb \| dbroweval \_mean = sprintf("%8.0f", \_mean); \_stddev =
sprintf("%8.0f", \_stddev);

Output:
-------

#fsdb size mean stddev pct_rsd 1024 1496200 284970 19.047 10240 5028600
601030 11.952 102400 4921600 309390 6.2863 # \| dbsetheader size bw # \|
/home/johnh/BIN/DB/dbmultistats size bw # \| /home/johnh/BIN/DB/dbcol
size mean stddev pct_rsd # \| /home/johnh/BIN/DB/dbroweval { \_mean =
sprintf("%8.0f", \_mean); \_stddev = sprintf("%8.0f", \_stddev); }

Command 2: Changing the Schema
------------------------------

By default, dbroweval reads and writes the same format file. The
recommended method of adding and removing columns is to do so before or
after dbroweval. I.e.,

cat data.fsdb \| dbcolcreate divisible_by_ten \| dbroweval
\_divisible_by_ten = (_size % 10 == 0); \| dbrow \_divisible_by_ten == 1
\| dbcol size mean divisible_by_ten

Another approach is to use the ``next row`` command to skip output of a
row. I.e., the equivalent:

cat data.fsdb \| dbcolcreate divisible_by_ten \| dbroweval
\_divisible_by_ten = (_size % 10 == 0); next row if
(!_divisible_by_ten); \| dbcol size mean divisible_by_ten

However, neither of these approachs work very well when the output is a
*completely* different schema.

The recommended method for schema-changing commands is to write a full
filter, but a full filter is a bit heavy weight. As an alternative, one
can use the ``-m`` option to request manual configuration of the output,
then use ``@out_args`` to define the output schema (it specifies the
``Fsdb::IO::Writer`` arguments), and ``$ofref`` is the output row. It
may also reference <$in>, the input ``Fsdb::IO::Reader`` argument, and
<$fref> as an aref to the current line. Note that newly created columns
*do not* have underscore-names

Thus a third equivalent is:

cat data.fsdb \| \\ dbroweval -m -b @out_args = ( -clone => $in, \\
-cols => ($in->cols, divisible_by_ten); \\ my $div_by_10 = (_size % 10
-- 0); \\ $ofref = [ @$fref, $div_by_10 ] if ($div_by_ten); \| dbcol
size mean divisible_by_ten

or

cat data.fsdb \| \\ dbroweval -m -b @out_args = ( -clone => $in, \\
-cols => [qw(size mean divisible_by_ten)] ); \\ my $div_by_10 = (_size %
10 == 0); \\ $ofref = [ \_mean, \_size, $div_by_10 ] if ($div_by_ten);

Finally, one can write different a completely different schema, although
it's more work:

cat data.fsdb \| \\ dbroweval -m -b @out_args = (-cols => [qw(size n)]);
\\ $ofref = [ \_size, 1 ];

writes different columns, and

cat data.fsdb \| \\ dbroweval -n -m -b @out_args = (-cols => [qw(n)]);
\\ my $count = 0; -e $ofref = [ $count ]; $count++;

Is a fancy way to count lines.

The begin code block should setup ``@out_args`` to be the arguments to a
``Fsdb::IO::Writer::new`` call, and whatever is in ``$ofref`` (if
anything) is written for each input line, and once at the end.

Command 3: Fun With Suppressing Output
--------------------------------------

The ``-n`` option suppresses default output. Thus, a simple equivalent
to *tail -1* is:

dbroweval -n -e $ofref = $lfref;

Where ``$ofref`` is the output fields, which are copied from ``$lfref``,
the hereby documented internal representation of the last row. Yes, this
is a bit unappetizing, but, in for a penny with ``$ofref``, in for a
pound.

Command 4: Extra Ouptut
-----------------------

Calling ``&$write_fastpath_sub($fref)`` will do extra output, so this
simple program will duplicate each line of input (one extra output, plus
one regular output for each line of input):

dbroweval &$write_fastpath_sub($fref)

BUGS
----

Handling of code in files isn't very elegant.

SEE ALSO
--------

**Fsdb** (3)

AUTHOR and COPYRIGHT
--------------------

Copyright (C) 1991-2018 by John Heidemann <johnh@isi.edu>

This program is distributed under terms of the GNU general public
license, version 2. See the file COPYING with the distribution for
details.
