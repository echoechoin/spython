
.. _restricted:

********************
Restricted Execution
********************

.. warning::

   In Python 2.3 these modules have been disabled due to various known and not
   readily fixable security holes.  The modules are still documented here to help
   in reading old code that uses the :mod:`rexec` and :mod:`Bastion` modules.

*Restricted execution* is the basic framework in Python that allows for the
segregation of trusted and untrusted code.  The framework is based on the notion
that trusted Python code (a *supervisor*) can create a "padded cell' (or
environment) with limited permissions, and run the untrusted code within this
cell.  The untrusted code cannot break out of its cell, and can only interact
with sensitive system resources through interfaces defined and managed by the
trusted code.  The term "restricted execution" is favored over "safe-Python"
since true safety is hard to define, and is determined by the way the restricted
environment is created.  Note that the restricted environments can be nested,
with inner cells creating subcells of lesser, but never greater, privilege.

An interesting aspect of Python's restricted execution model is that the
interfaces presented to untrusted code usually have the same names as those
presented to trusted code.  Therefore no special interfaces need to be learned
to write code designed to run in a restricted environment.  And because the
exact nature of the padded cell is determined by the supervisor, different
restrictions can be imposed, depending on the application.  For example, it
might be deemed "safe" for untrusted code to read any file within a specified
directory, but never to write a file.  In this case, the supervisor may redefine
the built-in :func:`open` function so that it raises an exception whenever the
*mode* parameter is ``'w'``.  It might also perform a :c:func:`chroot`\ -like
operation on the *filename* parameter, such that root is always relative to some
safe "sandbox" area of the filesystem.  In this case, the untrusted code would
still see a built-in :func:`open` function in its environment, with the same
calling interface.  The semantics would be identical too, with :exc:`IOError`\ s
being raised when the supervisor determined that an unallowable parameter is
being used.

The Python run-time determines whether a particular code block is executing in
restricted execution mode based on the identity of the ``__builtins__`` object
in its global variables: if this is (the dictionary of) the standard
:mod:`__builtin__` module, the code is deemed to be unrestricted, else it is
deemed to be restricted.

Python code executing in restricted mode faces a number of limitations that are
designed to prevent it from escaping from the padded cell. For instance, the
function object attribute :attr:`func_globals` and the class and instance object
attribute :attr:`~object.__dict__` are unavailable.

Two modules provide the framework for setting up restricted execution
environments:


.. toctree::

   rexec.rst
   bastion.rst

.. seealso::

   `Grail Home Page <http://grail.sourceforge.net/>`_
      Grail, an Internet browser written in Python, uses these modules to support
      Python applets.  More information on the use of Python's restricted execution
      mode in Grail is available on the Web site.

