:mod:`zipfile` --- Work with ZIP archives
=========================================

.. module:: zipfile
   :synopsis: Read and write ZIP-format archive files.
.. moduleauthor:: James C. Ahlstrom <jim@interet.com>
.. sectionauthor:: James C. Ahlstrom <jim@interet.com>

.. versionadded:: 1.6

**Source code:** :source:`Lib/zipfile.py`

--------------

The ZIP file format is a common archive and compression standard. This module
provides tools to create, read, write, append, and list a ZIP file.  Any
advanced use of this module will require an understanding of the format, as
defined in `PKZIP Application Note`_.

This module does not currently handle multi-disk ZIP files.
It can handle ZIP files that use the ZIP64 extensions
(that is ZIP files that are more than 4 GByte in size).  It supports
decryption of encrypted files in ZIP archives, but it currently cannot
create an encrypted file.  Decryption is extremely slow as it is
implemented in native Python rather than C.

The module defines the following items:

.. exception:: BadZipfile

   The error raised for bad ZIP files (old name: ``zipfile.error``).


.. exception:: LargeZipFile

   The error raised when a ZIP file would require ZIP64 functionality but that has
   not been enabled.


.. class:: ZipFile
   :noindex:

   The class for reading and writing ZIP files.  See section
   :ref:`zipfile-objects` for constructor details.


.. class:: PyZipFile

   Class for creating ZIP archives containing Python libraries.


.. class:: ZipInfo([filename[, date_time]])

   Class used to represent information about a member of an archive. Instances
   of this class are returned by the :meth:`.getinfo` and :meth:`.infolist`
   methods of :class:`ZipFile` objects.  Most users of the :mod:`zipfile` module
   will not need to create these, but only use those created by this
   module. *filename* should be the full name of the archive member, and
   *date_time* should be a tuple containing six fields which describe the time
   of the last modification to the file; the fields are described in section
   :ref:`zipinfo-objects`.


.. function:: is_zipfile(filename)

   Returns ``True`` if *filename* is a valid ZIP file based on its magic number,
   otherwise returns ``False``.  *filename* may be a file or file-like object too.

   .. versionchanged:: 2.7
      Support for file and file-like objects.

.. data:: ZIP_STORED

   The numeric constant for an uncompressed archive member.


.. data:: ZIP_DEFLATED

   The numeric constant for the usual ZIP compression method.  This requires the
   :mod:`zlib` module.  No other compression methods are currently supported.


.. seealso::

   `PKZIP Application Note`_
      Documentation on the ZIP file format by Phil Katz, the creator of the format and
      algorithms used.

   `Info-ZIP Home Page <http://www.info-zip.org/>`_
      Information about the Info-ZIP project's ZIP archive programs and development
      libraries.


.. _zipfile-objects:

ZipFile Objects
---------------


.. class:: ZipFile(file[, mode[, compression[, allowZip64]]])

   Open a ZIP file, where *file* can be either a path to a file (a string) or a
   file-like object.  The *mode* parameter should be ``'r'`` to read an existing
   file, ``'w'`` to truncate and write a new file, or ``'a'`` to append to an
   existing file.  If *mode* is ``'a'`` and *file* refers to an existing ZIP
   file, then additional files are added to it.  If *file* does not refer to a
   ZIP file, then a new ZIP archive is appended to the file.  This is meant for
   adding a ZIP archive to another file (such as :file:`python.exe`).

   .. versionchanged:: 2.6
      If *mode* is ``a`` and the file does not exist at all, it is created.

   *compression* is the ZIP compression method to use when writing the archive,
   and should be :const:`ZIP_STORED` or :const:`ZIP_DEFLATED`; unrecognized
   values will cause :exc:`RuntimeError` to be raised.  If :const:`ZIP_DEFLATED`
   is specified but the :mod:`zlib` module is not available, :exc:`RuntimeError`
   is also raised. The default is :const:`ZIP_STORED`.  If *allowZip64* is
   ``True`` zipfile will create ZIP files that use the ZIP64 extensions when
   the zipfile is larger than 2 GB. If it is  false (the default) :mod:`zipfile`
   will raise an exception when the ZIP file would require ZIP64 extensions.
   ZIP64 extensions are disabled by default because the default :program:`zip`
   and :program:`unzip` commands on Unix (the InfoZIP utilities) don't support
   these extensions.

   .. versionchanged:: 2.7.1
      If the file is created with mode ``'a'`` or ``'w'`` and then
      :meth:`closed <close>` without adding any files to the archive, the appropriate
      ZIP structures for an empty archive will be written to the file.

   ZipFile is also a context manager and therefore supports the
   :keyword:`with` statement.  In the example, *myzip* is closed after the
   :keyword:`with` statement's suite is finished---even if an exception occurs::

      with ZipFile('spam.zip', 'w') as myzip:
          myzip.write('eggs.txt')

   .. versionadded:: 2.7
      Added the ability to use :class:`ZipFile` as a context manager.


.. method:: ZipFile.close()

   Close the archive file.  You must call :meth:`close` before exiting your program
   or essential records will not be written.


.. method:: ZipFile.getinfo(name)

   Return a :class:`ZipInfo` object with information about the archive member
   *name*.  Calling :meth:`getinfo` for a name not currently contained in the
   archive will raise a :exc:`KeyError`.


.. method:: ZipFile.infolist()

   Return a list containing a :class:`ZipInfo` object for each member of the
   archive.  The objects are in the same order as their entries in the actual ZIP
   file on disk if an existing archive was opened.


.. method:: ZipFile.namelist()

   Return a list of archive members by name.

   .. index::
      single: universal newlines; zipfile.ZipFile.open method


.. method:: ZipFile.open(name[, mode[, pwd]])

   Extract a member from the archive as a file-like object (ZipExtFile). *name* is
   the name of the file in the archive, or a :class:`ZipInfo` object. The *mode*
   parameter, if included, must be one of the following: ``'r'`` (the default),
   ``'U'``, or ``'rU'``. Choosing ``'U'`` or  ``'rU'`` will enable
   :term:`universal newline <universal newlines>`
   support in the read-only object. *pwd* is the password used for encrypted files.
   Calling  :meth:`.open` on a closed ZipFile will raise a  :exc:`RuntimeError`.

   .. note::

      The file-like object is read-only and provides the following methods:
      :meth:`~file.read`, :meth:`~file.readline`,
      :meth:`~file.readlines`, :meth:`__iter__`,
      :meth:`~object.next`.

   .. note::

      If the ZipFile was created by passing in a file-like object as the  first
      argument to the constructor, then the object returned by :meth:`.open` shares the
      ZipFile's file pointer.  Under these  circumstances, the object returned by
      :meth:`.open` should not  be used after any additional operations are performed
      on the  ZipFile object.  If the ZipFile was created by passing in a string (the
      filename) as the first argument to the constructor, then  :meth:`.open` will
      create a new file object that will be held by the ZipExtFile, allowing it to
      operate independently of the  ZipFile.

   .. note::

      The :meth:`.open`, :meth:`read` and :meth:`extract` methods can take a filename
      or a :class:`ZipInfo` object.  You will appreciate this when trying to read a
      ZIP file that contains members with duplicate names.

   .. versionadded:: 2.6


.. method:: ZipFile.extract(member[, path[, pwd]])

   Extract a member from the archive to the current working directory; *member*
   must be its full name or a :class:`ZipInfo` object).  Its file information is
   extracted as accurately as possible.  *path* specifies a different directory
   to extract to.  *member* can be a filename or a :class:`ZipInfo` object.
   *pwd* is the password used for encrypted files.

   Returns the normalized path created (a directory or new file).

   .. versionadded:: 2.6

   .. note::

      If a member filename is an absolute path, a drive/UNC sharepoint and
      leading (back)slashes will be stripped, e.g.: ``///foo/bar`` becomes
      ``foo/bar`` on Unix, and ``C:\foo\bar`` becomes ``foo\bar`` on Windows.
      And all ``".."`` components in a member filename will be removed, e.g.:
      ``../../foo../../ba..r`` becomes ``foo../ba..r``.  On Windows illegal
      characters (``:``, ``<``, ``>``, ``|``, ``"``, ``?``, and ``*``)
      replaced by underscore (``_``).


.. method:: ZipFile.extractall([path[, members[, pwd]]])

   Extract all members from the archive to the current working directory.  *path*
   specifies a different directory to extract to.  *members* is optional and must
   be a subset of the list returned by :meth:`namelist`.  *pwd* is the password
   used for encrypted files.

   .. warning::

      Never extract archives from untrusted sources without prior inspection.
      It is possible that files are created outside of *path*, e.g. members
      that have absolute filenames starting with ``"/"`` or filenames with two
      dots ``".."``.

   .. versionchanged:: 2.7.4
      The zipfile module attempts to prevent that.  See :meth:`extract` note.

   .. versionadded:: 2.6


.. method:: ZipFile.printdir()

   Print a table of contents for the archive to ``sys.stdout``.


.. method:: ZipFile.setpassword(pwd)

   Set *pwd* as default password to extract encrypted files.

   .. versionadded:: 2.6


.. method:: ZipFile.read(name[, pwd])

   Return the bytes of the file *name* in the archive.  *name* is the name of the
   file in the archive, or a :class:`ZipInfo` object.  The archive must be open for
   read or append. *pwd* is the password used for encrypted  files and, if specified,
   it will override the default password set with :meth:`setpassword`.  Calling
   :meth:`read` on a closed ZipFile  will raise a :exc:`RuntimeError`.

   .. versionchanged:: 2.6
      *pwd* was added, and *name* can now be a :class:`ZipInfo` object.


.. method:: ZipFile.testzip()

   Read all the files in the archive and check their CRC's and file headers.
   Return the name of the first bad file, or else return ``None``. Calling
   :meth:`testzip` on a closed ZipFile will raise a :exc:`RuntimeError`.


.. method:: ZipFile.write(filename[, arcname[, compress_type]])

   Write the file named *filename* to the archive, giving it the archive name
   *arcname* (by default, this will be the same as *filename*, but without a drive
   letter and with leading path separators removed).  If given, *compress_type*
   overrides the value given for the *compression* parameter to the constructor for
   the new entry.  The archive must be open with mode ``'w'`` or ``'a'`` -- calling
   :meth:`write` on a ZipFile created with mode ``'r'`` will raise a
   :exc:`RuntimeError`.  Calling  :meth:`write` on a closed ZipFile will raise a
   :exc:`RuntimeError`.

   .. note::

      There is no official file name encoding for ZIP files. If you have unicode file
      names, you must convert them to byte strings in your desired encoding before
      passing them to :meth:`write`. WinZip interprets all file names as encoded in
      CP437, also known as DOS Latin.

   .. note::

      Archive names should be relative to the archive root, that is, they should not
      start with a path separator.

   .. note::

      If ``arcname`` (or ``filename``, if ``arcname`` is  not given) contains a null
      byte, the name of the file in the archive will be truncated at the null byte.


.. method:: ZipFile.writestr(zinfo_or_arcname, bytes[, compress_type])

   Write the string *bytes* to the archive; *zinfo_or_arcname* is either the file
   name it will be given in the archive, or a :class:`ZipInfo` instance.  If it's
   an instance, at least the filename, date, and time must be given.  If it's a
   name, the date and time is set to the current date and time. The archive must be
   opened with mode ``'w'`` or ``'a'`` -- calling  :meth:`writestr` on a ZipFile
   created with mode ``'r'``  will raise a :exc:`RuntimeError`.  Calling
   :meth:`writestr` on a closed ZipFile will raise a :exc:`RuntimeError`.

   If given, *compress_type* overrides the value given for the *compression*
   parameter to the constructor for the new entry, or in the *zinfo_or_arcname*
   (if that is a :class:`ZipInfo` instance).

   .. note::

      When passing a :class:`ZipInfo` instance as the *zinfo_or_arcname* parameter,
      the compression method used will be that specified in the *compress_type*
      member of the given :class:`ZipInfo` instance.  By default, the
      :class:`ZipInfo` constructor sets this member to :const:`ZIP_STORED`.

   .. versionchanged:: 2.7
      The *compress_type* argument.

The following data attributes are also available:


.. attribute:: ZipFile.debug

   The level of debug output to use.  This may be set from ``0`` (the default, no
   output) to ``3`` (the most output).  Debugging information is written to
   ``sys.stdout``.

.. attribute:: ZipFile.comment

   The comment text associated with the ZIP file.  If assigning a comment to a
   :class:`ZipFile` instance created with mode 'a' or 'w', this should be a
   string no longer than 65535 bytes.  Comments longer than this will be
   truncated in the written archive when :meth:`.close` is called.

.. _pyzipfile-objects:

PyZipFile Objects
-----------------

The :class:`PyZipFile` constructor takes the same parameters as the
:class:`ZipFile` constructor.  Instances have one method in addition to those of
:class:`ZipFile` objects.


.. method:: PyZipFile.writepy(pathname[, basename])

   Search for files :file:`\*.py` and add the corresponding file to the archive.
   The corresponding file is a :file:`\*.pyo` file if available, else a
   :file:`\*.pyc` file, compiling if necessary.  If the pathname is a file, the
   filename must end with :file:`.py`, and just the (corresponding
   :file:`\*.py[co]`) file is added at the top level (no path information).  If the
   pathname is a file that does not end with :file:`.py`, a :exc:`RuntimeError`
   will be raised.  If it is a directory, and the directory is not a package
   directory, then all the files :file:`\*.py[co]` are added at the top level.  If
   the directory is a package directory, then all :file:`\*.py[co]` are added under
   the package name as a file path, and if any subdirectories are package
   directories, all of these are added recursively.  *basename* is intended for
   internal use only.  The :meth:`writepy` method makes archives with file names
   like this::

      string.pyc                                # Top level name
      test/__init__.pyc                         # Package directory
      test/test_support.pyc                          # Module test.test_support
      test/bogus/__init__.pyc                   # Subpackage directory
      test/bogus/myfile.pyc                     # Submodule test.bogus.myfile


.. _zipinfo-objects:

ZipInfo Objects
---------------

Instances of the :class:`ZipInfo` class are returned by the :meth:`.getinfo` and
:meth:`.infolist` methods of :class:`ZipFile` objects.  Each object stores
information about a single member of the ZIP archive.

Instances have the following attributes:


.. attribute:: ZipInfo.filename

   Name of the file in the archive.


.. attribute:: ZipInfo.date_time

   The time and date of the last modification to the archive member.  This is a
   tuple of six values:

   +-------+--------------------------+
   | Index | Value                    |
   +=======+==========================+
   | ``0`` | Year (>= 1980)           |
   +-------+--------------------------+
   | ``1`` | Month (one-based)        |
   +-------+--------------------------+
   | ``2`` | Day of month (one-based) |
   +-------+--------------------------+
   | ``3`` | Hours (zero-based)       |
   +-------+--------------------------+
   | ``4`` | Minutes (zero-based)     |
   +-------+--------------------------+
   | ``5`` | Seconds (zero-based)     |
   +-------+--------------------------+

   .. note::

      The ZIP file format does not support timestamps before 1980.


.. attribute:: ZipInfo.compress_type

   Type of compression for the archive member.


.. attribute:: ZipInfo.comment

   Comment for the individual archive member.


.. attribute:: ZipInfo.extra

   Expansion field data.  The `PKZIP Application Note`_ contains
   some comments on the internal structure of the data contained in this string.


.. attribute:: ZipInfo.create_system

   System which created ZIP archive.


.. attribute:: ZipInfo.create_version

   PKZIP version which created ZIP archive.


.. attribute:: ZipInfo.extract_version

   PKZIP version needed to extract archive.


.. attribute:: ZipInfo.reserved

   Must be zero.


.. attribute:: ZipInfo.flag_bits

   ZIP flag bits.


.. attribute:: ZipInfo.volume

   Volume number of file header.


.. attribute:: ZipInfo.internal_attr

   Internal attributes.


.. attribute:: ZipInfo.external_attr

   External file attributes.


.. attribute:: ZipInfo.header_offset

   Byte offset to the file header.


.. attribute:: ZipInfo.CRC

   CRC-32 of the uncompressed file.


.. attribute:: ZipInfo.compress_size

   Size of the compressed data.


.. attribute:: ZipInfo.file_size

   Size of the uncompressed file.


.. _zipfile-commandline:
.. program:: zipfile

Command-Line Interface
----------------------

The :mod:`zipfile` module provides a simple command-line interface to interact
with ZIP archives.

If you want to create a new ZIP archive, specify its name after the :option:`-c`
option and then list the filename(s) that should be included:

.. code-block:: shell-session

    $ python -m zipfile -c monty.zip spam.txt eggs.txt

Passing a directory is also acceptable:

.. code-block:: shell-session

    $ python -m zipfile -c monty.zip life-of-brian_1979/

If you want to extract a ZIP archive into the specified directory, use
the :option:`-e` option:

.. code-block:: shell-session

    $ python -m zipfile -e monty.zip target-dir/

For a list of the files in a ZIP archive, use the :option:`-l` option:

.. code-block:: shell-session

    $ python -m zipfile -l monty.zip


Command-line options
~~~~~~~~~~~~~~~~~~~~

.. cmdoption:: -l <zipfile>

   List files in a zipfile.

.. cmdoption:: -c <zipfile> <source1> ... <sourceN>

   Create zipfile from source files.

.. cmdoption:: -e <zipfile> <output_dir>

   Extract zipfile into target directory.

.. cmdoption:: -t <zipfile>

   Test whether the zipfile is valid or not.


.. _PKZIP Application Note: https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
