regex2fsdb - creates a FSDB file with regex matches in a file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``regex2fsdb`` takes a regular expression using groupings, a list of
column names, and creates an FSDB file from the results.  It takes
python `re` style regular expressions so regex components like `\w+`
will match words and `\s+` will match spaces.  Matches to be used
within the results should be encased in regex `()` grouping markers
that will turn into columns.

Note: python's `re` will start matching at the beginning of lines, so
you may need to prepend `.*` or similar to grab up until the start of
the first match, though this may be over greedy at times.

Example command usage 1
^^^^^^^^^^^^^^^^^^^^^^^

The following creates a list of group names and group ids from a unix
/etc/group file:

::

   $ regex2fsdb -r '(\w+):[^:]*:(\d+)' -c groupname groupid -- /etc/group

Example output 2
^^^^^^^^^^^^^^^^

(only 5 lines shown in the example)

::
   #fsdb -F t groupname:a groupid:a
   root    0
   bin     1
   daemon  2
   sys     3
   adm     4

Example command usage 2
^^^^^^^^^^^^^^^^^^^^^^^

The following creates a list of mount points from ext4 or swap from an
/etc/fstab file:

::

   $ regex2fsdb -r '.*\s+([\w/]+)\s+(ext4|swap|vfat).*' -c point type -- /etc/fstab

Example output 2
^^^^^^^^^^^^^^^^

::

   #fsdb -F t point:a type:a
   /       ext4
   /boot   ext4
   /boot/efi       vfat
   /home   ext4
   none    swap
