.. highlightlang:: c

.. _importing:

Importing Modules
=================


.. c:function:: PyObject* PyImport_ImportModule(const char *name)

   .. index::
      single: package variable; __all__
      single: __all__ (package variable)
      single: modules (in module sys)

   This is a simplified interface to :c:func:`PyImport_ImportModuleEx` below,
   leaving the *globals* and *locals* arguments set to *NULL* and *level* set
   to 0.  When the *name*
   argument contains a dot (when it specifies a submodule of a package), the
   *fromlist* argument is set to the list ``['*']`` so that the return value is the
   named module rather than the top-level package containing it as would otherwise
   be the case.  (Unfortunately, this has an additional side effect when *name* in
   fact specifies a subpackage instead of a submodule: the submodules specified in
   the package's ``__all__`` variable are  loaded.)  Return a new reference to the
   imported module, or *NULL* with an exception set on failure.  Before Python 2.4,
   the module may still be created in the failure case --- examine ``sys.modules``
   to find out.  Starting with Python 2.4, a failing import of a module no longer
   leaves the module in ``sys.modules``.

   .. versionchanged:: 2.4
      Failing imports remove incomplete module objects.

   .. versionchanged:: 2.6
      Always uses absolute imports.


.. c:function:: PyObject* PyImport_ImportModuleNoBlock(const char *name)

   This version of :c:func:`PyImport_ImportModule` does not block. It's intended
   to be used in C functions that import other modules to execute a function.
   The import may block if another thread holds the import lock. The function
   :c:func:`PyImport_ImportModuleNoBlock` never blocks. It first tries to fetch
   the module from sys.modules and falls back to :c:func:`PyImport_ImportModule`
   unless the lock is held, in which case the function will raise an
   :exc:`ImportError`.

   .. versionadded:: 2.6


.. c:function:: PyObject* PyImport_ImportModuleEx(char *name, PyObject *globals, PyObject *locals, PyObject *fromlist)

   .. index:: builtin: __import__

   Import a module.  This is best described by referring to the built-in Python
   function :func:`__import__`, as the standard :func:`__import__` function calls
   this function directly.

   The return value is a new reference to the imported module or top-level package,
   or *NULL* with an exception set on failure (before Python 2.4, the module may
   still be created in this case).  Like for :func:`__import__`, the return value
   when a submodule of a package was requested is normally the top-level package,
   unless a non-empty *fromlist* was given.

   .. versionchanged:: 2.4
      Failing imports remove incomplete module objects.

   .. versionchanged:: 2.6
      The function is an alias for :c:func:`PyImport_ImportModuleLevel` with
      ``-1`` as level, meaning relative import.


.. c:function:: PyObject* PyImport_ImportModuleLevel(char *name, PyObject *globals, PyObject *locals, PyObject *fromlist, int level)

   Import a module.  This is best described by referring to the built-in Python
   function :func:`__import__`, as the standard :func:`__import__` function calls
   this function directly.

   The return value is a new reference to the imported module or top-level package,
   or *NULL* with an exception set on failure.  Like for :func:`__import__`,
   the return value when a submodule of a package was requested is normally the
   top-level package, unless a non-empty *fromlist* was given.

   .. versionadded:: 2.5


.. c:function:: PyObject* PyImport_Import(PyObject *name)

   .. index::
      module: rexec
      module: ihooks

   This is a higher-level interface that calls the current "import hook function".
   It invokes the :func:`__import__` function from the ``__builtins__`` of the
   current globals.  This means that the import is done using whatever import hooks
   are installed in the current environment, e.g. by :mod:`rexec` or :mod:`ihooks`.

   .. versionchanged:: 2.6
      Always uses absolute imports.


.. c:function:: PyObject* PyImport_ReloadModule(PyObject *m)

   .. index:: builtin: reload

   Reload a module.  This is best described by referring to the built-in Python
   function :func:`reload`, as the standard :func:`reload` function calls this
   function directly.  Return a new reference to the reloaded module, or *NULL*
   with an exception set on failure (the module still exists in this case).


.. c:function:: PyObject* PyImport_AddModule(const char *name)

   Return the module object corresponding to a module name.  The *name* argument
   may be of the form ``package.module``. First check the modules dictionary if
   there's one there, and if not, create a new one and insert it in the modules
   dictionary. Return *NULL* with an exception set on failure.

   .. note::

      This function does not load or import the module; if the module wasn't already
      loaded, you will get an empty module object. Use :c:func:`PyImport_ImportModule`
      or one of its variants to import a module.  Package structures implied by a
      dotted name for *name* are not created if not already present.


.. c:function:: PyObject* PyImport_ExecCodeModule(char *name, PyObject *co)

   .. index:: builtin: compile

   Given a module name (possibly of the form ``package.module``) and a code object
   read from a Python bytecode file or obtained from the built-in function
   :func:`compile`, load the module.  Return a new reference to the module object,
   or *NULL* with an exception set if an error occurred.  Before Python 2.4, the
   module could still be created in error cases.  Starting with Python 2.4, *name*
   is removed from :attr:`sys.modules` in error cases, and even if *name* was already
   in :attr:`sys.modules` on entry to :c:func:`PyImport_ExecCodeModule`.  Leaving
   incompletely initialized modules in :attr:`sys.modules` is dangerous, as imports of
   such modules have no way to know that the module object is an unknown (and
   probably damaged with respect to the module author's intents) state.

   The module's :attr:`__file__` attribute will be set to the code object's
   :c:member:`co_filename`.

   This function will reload the module if it was already imported.  See
   :c:func:`PyImport_ReloadModule` for the intended way to reload a module.

   If *name* points to a dotted name of the form ``package.module``, any package
   structures not already created will still not be created.

   .. versionchanged:: 2.4
      *name* is removed from :attr:`sys.modules` in error cases.


.. c:function:: PyObject* PyImport_ExecCodeModuleEx(char *name, PyObject *co, char *pathname)

   Like :c:func:`PyImport_ExecCodeModule`, but the :attr:`__file__` attribute of
   the module object is set to *pathname* if it is non-``NULL``.


.. c:function:: long PyImport_GetMagicNumber()

   Return the magic number for Python bytecode files (a.k.a. :file:`.pyc` and
   :file:`.pyo` files).  The magic number should be present in the first four bytes
   of the bytecode file, in little-endian byte order.


.. c:function:: PyObject* PyImport_GetModuleDict()

   Return the dictionary used for the module administration (a.k.a.
   ``sys.modules``).  Note that this is a per-interpreter variable.


.. c:function:: PyObject* PyImport_GetImporter(PyObject *path)

   Return an importer object for a :data:`sys.path`/:attr:`pkg.__path__` item
   *path*, possibly by fetching it from the :data:`sys.path_importer_cache`
   dict.  If it wasn't yet cached, traverse :data:`sys.path_hooks` until a hook
   is found that can handle the path item.  Return ``None`` if no hook could;
   this tells our caller it should fall back to the built-in import mechanism.
   Cache the result in :data:`sys.path_importer_cache`.  Return a new reference
   to the importer object.

   .. versionadded:: 2.6


.. c:function:: void _PyImport_Init()

   Initialize the import mechanism.  For internal use only.


.. c:function:: void PyImport_Cleanup()

   Empty the module table.  For internal use only.


.. c:function:: void _PyImport_Fini()

   Finalize the import mechanism.  For internal use only.


.. c:function:: PyObject* _PyImport_FindExtension(char *, char *)

   For internal use only.


.. c:function:: PyObject* _PyImport_FixupExtension(char *, char *)

   For internal use only.


.. c:function:: int PyImport_ImportFrozenModule(char *name)

   Load a frozen module named *name*.  Return ``1`` for success, ``0`` if the
   module is not found, and ``-1`` with an exception set if the initialization
   failed.  To access the imported module on a successful load, use
   :c:func:`PyImport_ImportModule`.  (Note the misnomer --- this function would
   reload the module if it was already imported.)


.. c:type:: struct _frozen

   .. index:: single: freeze utility

   This is the structure type definition for frozen module descriptors, as
   generated by the :program:`freeze` utility (see :file:`Tools/freeze/` in the
   Python source distribution).  Its definition, found in :file:`Include/import.h`,
   is::

      struct _frozen {
          char *name;
          unsigned char *code;
          int size;
      };


.. c:var:: struct _frozen* PyImport_FrozenModules

   This pointer is initialized to point to an array of :c:type:`struct _frozen`
   records, terminated by one whose members are all *NULL* or zero.  When a frozen
   module is imported, it is searched in this table.  Third-party code could play
   tricks with this to provide a dynamically created collection of frozen modules.


.. c:function:: int PyImport_AppendInittab(const char *name, void (*initfunc)(void))

   Add a single module to the existing table of built-in modules.  This is a
   convenience wrapper around :c:func:`PyImport_ExtendInittab`, returning ``-1`` if
   the table could not be extended.  The new module can be imported by the name
   *name*, and uses the function *initfunc* as the initialization function called
   on the first attempted import.  This should be called before
   :c:func:`Py_Initialize`.


.. c:type:: struct _inittab

   Structure describing a single entry in the list of built-in modules.  Each of
   these structures gives the name and initialization function for a module built
   into the interpreter.  Programs which embed Python may use an array of these
   structures in conjunction with :c:func:`PyImport_ExtendInittab` to provide
   additional built-in modules.  The structure is defined in
   :file:`Include/import.h` as::

      struct _inittab {
          char *name;
          void (*initfunc)(void);
      };


.. c:function:: int PyImport_ExtendInittab(struct _inittab *newtab)

   Add a collection of modules to the table of built-in modules.  The *newtab*
   array must end with a sentinel entry which contains *NULL* for the :attr:`name`
   field; failure to provide the sentinel value can result in a memory fault.
   Returns ``0`` on success or ``-1`` if insufficient memory could be allocated to
   extend the internal table.  In the event of failure, no modules are added to the
   internal table.  This should be called before :c:func:`Py_Initialize`.
