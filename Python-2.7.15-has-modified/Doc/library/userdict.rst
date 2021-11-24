:mod:`UserDict` --- Class wrapper for dictionary objects
========================================================

.. module:: UserDict
   :synopsis: Class wrapper for dictionary objects.


**Source code:** :source:`Lib/UserDict.py`

--------------

The module defines a mixin,  :class:`DictMixin`, defining all dictionary methods
for classes that already have a minimum mapping interface.  This greatly
simplifies writing classes that need to be substitutable for dictionaries (such
as the shelve module).

This module also defines a class, :class:`~UserDict.UserDict`, that acts as a wrapper
around dictionary objects.  The need for this class has been largely supplanted
by the ability to subclass directly from :class:`dict` (a feature that became
available starting with Python version 2.2).  Prior to the introduction of
:class:`dict`, the :class:`~UserDict.UserDict` class was used to create dictionary-like
sub-classes that obtained new behaviors by overriding existing methods or adding
new ones.

The :mod:`UserDict` module defines the :class:`~UserDict.UserDict` class and
:class:`DictMixin`:


.. class:: UserDict([initialdata])

   Class that simulates a dictionary.  The instance's contents are kept in a
   regular dictionary, which is accessible via the :attr:`data` attribute of
   :class:`~UserDict.UserDict` instances.  If *initialdata* is provided, :attr:`data` is
   initialized with its contents; note that a reference to *initialdata* will not
   be kept, allowing it be used for other purposes.

   .. note::

      For backward compatibility, instances of :class:`~UserDict.UserDict` are not iterable.


.. class:: IterableUserDict([initialdata])

   Subclass of :class:`~UserDict.UserDict` that supports direct iteration (e.g.  ``for key in
   myDict``).

In addition to supporting the methods and operations of mappings (see section
:ref:`typesmapping`), :class:`~UserDict.UserDict` and :class:`IterableUserDict` instances
provide the following attribute:


.. attribute:: IterableUserDict.data

   A real dictionary used to store the contents of the :class:`~UserDict.UserDict` class.


.. class:: DictMixin()

   Mixin defining all dictionary methods for classes that already have a minimum
   dictionary interface including :meth:`__getitem__`, :meth:`__setitem__`,
   :meth:`__delitem__`, and :meth:`keys`.

   This mixin should be used as a superclass.  Adding each of the above methods
   adds progressively more functionality.  For instance, defining all but
   :meth:`__delitem__` will preclude only :meth:`pop` and :meth:`popitem` from the
   full interface.

   In addition to the four base methods, progressively more efficiency comes with
   defining :meth:`__contains__`, :meth:`__iter__`, and :meth:`iteritems`.

   Since the mixin has no knowledge of the subclass constructor, it does not define
   :meth:`__init__` or :meth:`copy`.

   Starting with Python version 2.6, it is recommended to use
   :class:`collections.MutableMapping` instead of :class:`DictMixin`.

   Note that DictMixin does not implement the :meth:`~dict.viewkeys`,
   :meth:`~dict.viewvalues`, or :meth:`~dict.viewitems` methods.

:mod:`UserList` --- Class wrapper for list objects
==================================================

.. module:: UserList
   :synopsis: Class wrapper for list objects.


.. note::

   When Python 2.2 was released, many of the use cases for this class were
   subsumed by the ability to subclass :class:`list` directly.  However, a
   handful of use cases remain.

   This module provides a list-interface around an underlying data store.  By
   default, that data store is a :class:`list`; however, it can be used to wrap
   a list-like interface around other objects (such as persistent storage).

   In addition, this class can be mixed-in with built-in classes using multiple
   inheritance.  This can sometimes be useful.  For example, you can inherit
   from :class:`~UserList.UserList` and :class:`str` at the same time.  That would not be
   possible with both a real :class:`list` and a real :class:`str`.

This module defines a class that acts as a wrapper around list objects.  It is a
useful base class for your own list-like classes, which can inherit from them
and override existing methods or add new ones.  In this way one can add new
behaviors to lists.

The :mod:`UserList` module defines the :class:`~UserList.UserList` class:


.. class:: UserList([list])

   Class that simulates a list.  The instance's contents are kept in a regular
   list, which is accessible via the :attr:`data` attribute of :class:`~UserList.UserList`
   instances.  The instance's contents are initially set to a copy of *list*,
   defaulting to the empty list ``[]``.  *list* can be any iterable, e.g. a
   real Python list or a :class:`~UserList.UserList` object.

   .. note::
      The :class:`~UserList.UserList` class has been moved to the :mod:`collections`
      module in Python 3. The :term:`2to3` tool will automatically adapt
      imports when converting your sources to Python 3.


In addition to supporting the methods and operations of mutable sequences (see
section :ref:`typesseq`), :class:`~UserList.UserList` instances provide the following
attribute:


.. attribute:: UserList.data

   A real Python list object used to store the contents of the :class:`~UserList.UserList`
   class.

**Subclassing requirements:** Subclasses of :class:`~UserList.UserList` are expected to
offer a constructor which can be called with either no arguments or one
argument.  List operations which return a new sequence attempt to create an
instance of the actual implementation class.  To do so, it assumes that the
constructor can be called with a single parameter, which is a sequence object
used as a data source.

If a derived class does not wish to comply with this requirement, all of the
special methods supported by this class will need to be overridden; please
consult the sources for information about the methods which need to be provided
in that case.

.. versionchanged:: 2.0
   Python versions 1.5.2 and 1.6 also required that the constructor be callable
   with no parameters, and offer a mutable :attr:`data` attribute.  Earlier
   versions of Python did not attempt to create instances of the derived class.


:mod:`UserString` --- Class wrapper for string objects
======================================================

.. module:: UserString
   :synopsis: Class wrapper for string objects.
.. moduleauthor:: Peter Funk <pf@artcom-gmbh.de>
.. sectionauthor:: Peter Funk <pf@artcom-gmbh.de>


.. note::

   This :class:`~UserString.UserString` class from this module is available for backward
   compatibility only.  If you are writing code that does not need to work with
   versions of Python earlier than Python 2.2, please consider subclassing directly
   from the built-in :class:`str` type instead of using :class:`~UserString.UserString` (there
   is no built-in equivalent to :class:`MutableString`).

This module defines a class that acts as a wrapper around string objects.  It is
a useful base class for your own string-like classes, which can inherit from
them and override existing methods or add new ones.  In this way one can add new
behaviors to strings.

It should be noted that these classes are highly inefficient compared to real
string or Unicode objects; this is especially the case for
:class:`MutableString`.

The :mod:`UserString` module defines the following classes:


.. class:: UserString([sequence])

   Class that simulates a string or a Unicode string object.  The instance's
   content is kept in a regular string or Unicode string object, which is
   accessible via the :attr:`data` attribute of :class:`~UserString.UserString` instances.  The
   instance's contents are initially set to a copy of *sequence*.  *sequence* can
   be either a regular Python string or Unicode string, an instance of
   :class:`~UserString.UserString` (or a subclass) or an arbitrary sequence which can be
   converted into a string using the built-in :func:`str` function.

   .. note::
      The :class:`~UserString.UserString` class has been moved to the :mod:`collections`
      module in Python 3. The :term:`2to3` tool will automatically adapt
      imports when converting your sources to Python 3.



.. class:: MutableString([sequence])

   This class is derived from the :class:`~UserString.UserString` above and redefines strings
   to be *mutable*.  Mutable strings can't be used as dictionary keys, because
   dictionaries require *immutable* objects as keys.  The main intention of this
   class is to serve as an educational example for inheritance and necessity to
   remove (override) the :meth:`__hash__` method in order to trap attempts to use a
   mutable object as dictionary key, which would be otherwise very error prone and
   hard to track down.

   .. deprecated:: 2.6
      The :class:`MutableString` class has been removed in Python 3.

In addition to supporting the methods and operations of string and Unicode
objects (see section :ref:`string-methods`), :class:`~UserString.UserString` instances
provide the following attribute:


.. attribute:: MutableString.data

   A real Python string or Unicode object used to store the content of the
   :class:`~UserString.UserString` class.

