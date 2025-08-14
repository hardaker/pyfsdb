PyFSDB Command Line Tools
=========================

The following shell tools come with PyFSDB and can be used for generic
command line processing of FSDB data.  We break the list of tools up
into different categories (although some tools may technical belong to
multiple categories, we place them in only one).

Note: the `python` based tools begin with the `pdb` prefix to
distinguish themselves from their `perl` counter-parts (which begin
with `db`).


Data filtering and modification tools
-------------------------------------

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   pdbrow
   pdbroweval
   pdbensure
   pdbaugment
   pdbfgrep
   pdbnormalize
   pdbcdf
   pdbdatetoepoch
   pdbepochtodate
   pdbkeyedsort
   pdbsum
   pdbzerofill

Data conversion tools
---------------------

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   pdb2to1
   pdbaddtypes
   pdbformat
   pdbjinja
   pdb2tex
   pdb2sql
   pdbsplitter
   pdbfullpivot
   pdbreescape
   pdbpathtrack

Data analysis tools
-------------------

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   pdbcoluniq
   pdbtopn
   pdbheatmap
   pdbsankey
