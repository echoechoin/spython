.. highlightlang:: c

.. _stringobjects:

String/Bytes Objects
--------------------

These functions raise :exc:`TypeError` when expecting a string parameter and are
called with a non-string parameter.

.. note::

   These functions have been renamed to PyBytes_* in Python 3.x. Unless
   otherwise noted, the PyBytes functions available in 3.x are aliased to their
   PyString_* equivalents to help porting.

.. index:: object: string


.. c:type:: PyStringObject

   This subtype of :c:type:`PyObject` represents a Python string object.


.. c:var:: PyTypeObject PyString_Type

   .. index:: single: StringType (in module types)

   This instance of :c:type:`PyTypeObject` represents the Python string type; it is
   the same object as ``str`` and ``types.StringType`` in the Python layer. .


.. c:function:: int PyString_Check(PyObject *o)

   Return true if the object *o* is a string object or an instance of a subtype of
   the string type.

   .. versionchanged:: 2.2
      Allowed subtypes to be accepted.


.. c:function:: int PyString_CheckExact(PyObject *o)

   Return true if the object *o* is a string object, but not an instance of a
   subtype of the string type.

   .. versionadded:: 2.2


.. c:function:: PyObject* PyString_FromString(const char *v)

   Return a new string object with a copy of the string *v* as value on success,
   and *NULL* on failure.  The parameter *v* must not be *NULL*; it will not be
   checked.


.. c:function:: PyObject* PyString_FromStringAndSize(const char *v, Py_ssize_t len)

   Return a new string object with a copy of the string *v* as value and length
   *len* on success, and *NULL* on failure.  If *v* is *NULL*, the contents of the
   string are uninitialized.

   .. versionchanged:: 2.5
      This function used an :c:type:`int` type for *len*. This might require
      changes in your code for properly supporting 64-bit systems.


.. c:function:: PyObject* PyString_FromFormat(const char *format, ...)

   Take a C :c:func:`printf`\ -style *format* string and a variable number of
   arguments, calculate the size of the resulting Python string and return a string
   with the values formatted into it.  The variable arguments must be C types and
   must correspond exactly to the format characters in the *format* string.  The
   following format characters are allowed:

   .. % This should be exactly the same as the table in PyErr_Format.
   .. % One should just refer to the other.
   .. % The descriptions for %zd and %zu are wrong, but the truth is complicated
   .. % because not all compilers support the %z width modifier -- we fake it
   .. % when necessary via interpolating PY_FORMAT_SIZE_T.
   .. % Similar comments apply to the %ll width modifier and
   .. % PY_FORMAT_LONG_LONG.
   .. % %u, %lu, %zu should have "new in Python 2.5" blurbs.

   +-------------------+---------------+--------------------------------+
   | Format Characters | Type          | Comment                        |
   +===================+===============+================================+
   | :attr:`%%`        | *n/a*         | The literal % character.       |
   +-------------------+---------------+--------------------------------+
   | :attr:`%c`        | int           | A single character,            |
   |                   |               | represented as a C int.        |
   +-------------------+---------------+--------------------------------+
   | :attr:`%d`        | int           | Exactly equivalent to          |
   |                   |               | ``printf("%d")``.              |
   +-------------------+---------------+--------------------------------+
   | :attr:`%u`        | unsigned int  | Exactly equivalent to          |
   |                   |               | ``printf("%u")``.              |
   +-------------------+---------------+--------------------------------+
   | :attr:`%ld`       | long          | Exactly equivalent to          |
   |                   |               | ``printf("%ld")``.             |
   +-------------------+---------------+--------------------------------+
   | :attr:`%lu`       | unsigned long | Exactly equivalent to          |
   |                   |               | ``printf("%lu")``.             |
   +-------------------+---------------+--------------------------------+
   | :attr:`%lld`      | long long     | Exactly equivalent to          |
   |                   |               | ``printf("%lld")``.            |
   +-------------------+---------------+--------------------------------+
   | :attr:`%llu`      | unsigned      | Exactly equivalent to          |
   |                   | long long     | ``printf("%llu")``.            |
   +-------------------+---------------+--------------------------------+
   | :attr:`%zd`       | Py_ssize_t    | Exactly equivalent to          |
   |                   |               | ``printf("%zd")``.             |
   +-------------------+---------------+--------------------------------+
   | :attr:`%zu`       | size_t        | Exactly equivalent to          |
   |                   |               | ``printf("%zu")``.             |
   +-------------------+---------------+--------------------------------+
   | :attr:`%i`        | int           | Exactly equivalent to          |
   |                   |               | ``printf("%i")``.              |
   +-------------------+---------------+--------------------------------+
   | :attr:`%x`        | int           | Exactly equivalent to          |
   |                   |               | ``printf("%x")``.              |
   +-------------------+---------------+--------------------------------+
   | :attr:`%s`        | char\*        | A null-terminated C character  |
   |                   |               | array.                         |
   +-------------------+---------------+--------------------------------+
   | :attr:`%p`        | void\*        | The hex representation of a C  |
   |                   |               | pointer. Mostly equivalent to  |
   |                   |               | ``printf("%p")`` except that   |
   |                   |               | it is guaranteed to start with |
   |                   |               | the literal ``0x`` regardless  |
   |                   |               | of what the platform's         |
   |                   |               | ``printf`` yields.             |
   +-------------------+---------------+--------------------------------+

   An unrecognized format character causes all the rest of the format string to be
   copied as-is to the result string, and any extra arguments discarded.

   .. note::

      The `"%lld"` and `"%llu"` format specifiers are only available
      when :const:`HAVE_LONG_LONG` is defined.

   .. versionchanged:: 2.7
      Support for `"%lld"` and `"%llu"` added.


.. c:function:: PyObject* PyString_FromFormatV(const char *format, va_list vargs)

   Identical to :c:func:`PyString_FromFormat` except that it takes exactly two
   arguments.


.. c:function:: Py_ssize_t PyString_Size(PyObject *string)

   Return the length of the string in string object *string*.

   .. versionchanged:: 2.5
      This function returned an :c:type:`int` type. This might require changes
      in your code for properly supporting 64-bit systems.


.. c:function:: Py_ssize_t PyString_GET_SIZE(PyObject *string)

   Macro form of :c:func:`PyString_Size` but without error checking.

   .. versionchanged:: 2.5
      This macro returned an :c:type:`int` type. This might require changes in
      your code for properly supporting 64-bit systems.


.. c:function:: char* PyString_AsString(PyObject *string)

   Return a NUL-terminated representation of the contents of *string*.  The pointer
   refers to the internal buffer of *string*, not a copy.  The data must not be
   modified in any way, unless the string was just created using
   ``PyString_FromStringAndSize(NULL, size)``. It must not be deallocated.  If
   *string* is a Unicode object, this function computes the default encoding of
   *string* and operates on that.  If *string* is not a string object at all,
   :c:func:`PyString_AsString` returns *NULL* and raises :exc:`TypeError`.


.. c:function:: char* PyString_AS_STRING(PyObject *string)

   Macro form of :c:func:`PyString_AsString` but without error checking.  Only
   string objects are supported; no Unicode objects should be passed.


.. c:function:: int PyString_AsStringAndSize(PyObject *obj, char **buffer, Py_ssize_t *length)

   Return a NUL-terminated representation of the contents of the object *obj*
   through the output variables *buffer* and *length*.

   The function accepts both string and Unicode objects as input. For Unicode
   objects it returns the default encoded version of the object.  If *length* is
   *NULL*, the resulting buffer may not contain NUL characters; if it does, the
   function returns ``-1`` and a :exc:`TypeError` is raised.

   The buffer refers to an internal string buffer of *obj*, not a copy. The data
   must not be modified in any way, unless the string was just created using
   ``PyString_FromStringAndSize(NULL, size)``.  It must not be deallocated.  If
   *string* is a Unicode object, this function computes the default encoding of
   *string* and operates on that.  If *string* is not a string object at all,
   :c:func:`PyString_AsStringAndSize` returns ``-1`` and raises :exc:`TypeError`.

   .. versionchanged:: 2.5
      This function used an :c:type:`int *` type for *length*. This might
      require changes in your code for properly supporting 64-bit systems.


.. c:function:: void PyString_Concat(PyObject **string, PyObject *newpart)

   Create a new string object in *\*string* containing the contents of *newpart*
   appended to *string*; the caller will own the new reference.  The reference to
   the old value of *string* will be stolen.  If the new string cannot be created,
   the old reference to *string* will still be discarded and the value of
   *\*string* will be set to *NULL*; the appropriate exception will be set.


.. c:function:: void PyString_ConcatAndDel(PyObject **string, PyObject *newpart)

   Create a new string object in *\*string* containing the contents of *newpart*
   appended to *string*.  This version decrements the reference count of *newpart*.


.. c:function:: int _PyString_Resize(PyObject **string, Py_ssize_t newsize)

   A way to resize a string object even though it is "immutable". Only use this to
   build up a brand new string object; don't use this if the string may already be
   known in other parts of the code.  It is an error to call this function if the
   refcount on the input string object is not one. Pass the address of an existing
   string object as an lvalue (it may be written into), and the new size desired.
   On success, *\*string* holds the resized string object and ``0`` is returned;
   the address in *\*string* may differ from its input value.  If the reallocation
   fails, the original string object at *\*string* is deallocated, *\*string* is
   set to *NULL*, a memory exception is set, and ``-1`` is returned.

   .. versionchanged:: 2.5
      This function used an :c:type:`int` type for *newsize*. This might
      require changes in your code for properly supporting 64-bit systems.

.. c:function:: PyObject* PyString_Format(PyObject *format, PyObject *args)

   Return a new string object from *format* and *args*. Analogous to ``format %
   args``.  The *args* argument must be a tuple or dict.


.. c:function:: void PyString_InternInPlace(PyObject **string)

   Intern the argument *\*string* in place.  The argument must be the address of a
   pointer variable pointing to a Python string object.  If there is an existing
   interned string that is the same as *\*string*, it sets *\*string* to it
   (decrementing the reference count of the old string object and incrementing the
   reference count of the interned string object), otherwise it leaves *\*string*
   alone and interns it (incrementing its reference count).  (Clarification: even
   though there is a lot of talk about reference counts, think of this function as
   reference-count-neutral; you own the object after the call if and only if you
   owned it before the call.)

   .. note::

      This function is not available in 3.x and does not have a PyBytes alias.


.. c:function:: PyObject* PyString_InternFromString(const char *v)

   A combination of :c:func:`PyString_FromString` and
   :c:func:`PyString_InternInPlace`, returning either a new string object that has
   been interned, or a new ("owned") reference to an earlier interned string object
   with the same value.

   .. note::

      This function is not available in 3.x and does not have a PyBytes alias.


.. c:function:: PyObject* PyString_Decode(const char *s, Py_ssize_t size, const char *encoding, const char *errors)

   Create an object by decoding *size* bytes of the encoded buffer *s* using the
   codec registered for *encoding*.  *encoding* and *errors* have the same meaning
   as the parameters of the same name in the :func:`unicode` built-in function.
   The codec to be used is looked up using the Python codec registry.  Return
   *NULL* if an exception was raised by the codec.

   .. note::

      This function is not available in 3.x and does not have a PyBytes alias.

   .. versionchanged:: 2.5
      This function used an :c:type:`int` type for *size*. This might require
      changes in your code for properly supporting 64-bit systems.


.. c:function:: PyObject* PyString_AsDecodedObject(PyObject *str, const char *encoding, const char *errors)

   Decode a string object by passing it to the codec registered for *encoding* and
   return the result as Python object. *encoding* and *errors* have the same
   meaning as the parameters of the same name in the string :meth:`encode` method.
   The codec to be used is looked up using the Python codec registry. Return *NULL*
   if an exception was raised by the codec.

   .. note::

      This function is not available in 3.x and does not have a PyBytes alias.


.. c:function:: PyObject* PyString_Encode(const char *s, Py_ssize_t size, const char *encoding, const char *errors)

   Encode the :c:type:`char` buffer of the given size by passing it to the codec
   registered for *encoding* and return a Python object. *encoding* and *errors*
   have the same meaning as the parameters of the same name in the string
   :meth:`encode` method. The codec to be used is looked up using the Python codec
   registry.  Return *NULL* if an exception was raised by the codec.

   .. note::

      This function is not available in 3.x and does not have a PyBytes alias.

   .. versionchanged:: 2.5
      This function used an :c:type:`int` type for *size*. This might require
      changes in your code for properly supporting 64-bit systems.


.. c:function:: PyObject* PyString_AsEncodedObject(PyObject *str, const char *encoding, const char *errors)

   Encode a string object using the codec registered for *encoding* and return the
   result as Python object. *encoding* and *errors* have the same meaning as the
   parameters of the same name in the string :meth:`encode` method. The codec to be
   used is looked up using the Python codec registry. Return *NULL* if an exception
   was raised by the codec.

   .. note::

      This function is not available in 3.x and does not have a PyBytes alias.
