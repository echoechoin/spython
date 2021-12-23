
.. _datamodel:

**********
Data model
**********


.. _objects:

Objects, values and types
=========================

.. index::
   single: object
   single: data

:dfn:`Objects` are Python's abstraction for data.  All data in a Python program
is represented by objects or by relations between objects. (In a sense, and in
conformance to Von Neumann's model of a "stored program computer," code is also
represented by objects.)

.. index::
   builtin: id
   builtin: type
   single: identity of an object
   single: value of an object
   single: type of an object
   single: mutable object
   single: immutable object

Every object has an identity, a type and a value.  An object's *identity* never
changes once it has been created; you may think of it as the object's address in
memory.  The ':keyword:`is`' operator compares the identity of two objects; the
:func:`id` function returns an integer representing its identity (currently
implemented as its address). An object's :dfn:`type` is also unchangeable. [#]_
An object's type determines the operations that the object supports (e.g., "does
it have a length?") and also defines the possible values for objects of that
type.  The :func:`type` function returns an object's type (which is an object
itself).  The *value* of some objects can change.  Objects whose value can
change are said to be *mutable*; objects whose value is unchangeable once they
are created are called *immutable*. (The value of an immutable container object
that contains a reference to a mutable object can change when the latter's value
is changed; however the container is still considered immutable, because the
collection of objects it contains cannot be changed.  So, immutability is not
strictly the same as having an unchangeable value, it is more subtle.) An
object's mutability is determined by its type; for instance, numbers, strings
and tuples are immutable, while dictionaries and lists are mutable.

.. index::
   single: garbage collection
   single: reference counting
   single: unreachable object

Objects are never explicitly destroyed; however, when they become unreachable
they may be garbage-collected.  An implementation is allowed to postpone garbage
collection or omit it altogether --- it is a matter of implementation quality
how garbage collection is implemented, as long as no objects are collected that
are still reachable.

.. impl-detail::

   CPython currently uses a reference-counting scheme with (optional) delayed
   detection of cyclically linked garbage, which collects most objects as soon
   as they become unreachable, but is not guaranteed to collect garbage
   containing circular references.  See the documentation of the :mod:`gc`
   module for information on controlling the collection of cyclic garbage.
   Other implementations act differently and CPython may change.
   Do not depend on immediate finalization of objects when they become
   unreachable (ex: always close files).

Note that the use of the implementation's tracing or debugging facilities may
keep objects alive that would normally be collectable. Also note that catching
an exception with a ':keyword:`try`...\ :keyword:`except`' statement may keep
objects alive.

Some objects contain references to "external" resources such as open files or
windows.  It is understood that these resources are freed when the object is
garbage-collected, but since garbage collection is not guaranteed to happen,
such objects also provide an explicit way to release the external resource,
usually a :meth:`close` method. Programs are strongly recommended to explicitly
close such objects.  The ':keyword:`try`...\ :keyword:`finally`' statement
provides a convenient way to do this.

.. index:: single: container

Some objects contain references to other objects; these are called *containers*.
Examples of containers are tuples, lists and dictionaries.  The references are
part of a container's value.  In most cases, when we talk about the value of a
container, we imply the values, not the identities of the contained objects;
however, when we talk about the mutability of a container, only the identities
of the immediately contained objects are implied.  So, if an immutable container
(like a tuple) contains a reference to a mutable object, its value changes if
that mutable object is changed.

Types affect almost all aspects of object behavior.  Even the importance of
object identity is affected in some sense: for immutable types, operations that
compute new values may actually return a reference to any existing object with
the same type and value, while for mutable objects this is not allowed.  E.g.,
after ``a = 1; b = 1``, ``a`` and ``b`` may or may not refer to the same object
with the value one, depending on the implementation, but after ``c = []; d =
[]``, ``c`` and ``d`` are guaranteed to refer to two different, unique, newly
created empty lists. (Note that ``c = d = []`` assigns the same object to both
``c`` and ``d``.)


.. _types:

The standard type hierarchy
===========================

.. index::
   single: type
   pair: data; type
   pair: type; hierarchy
   pair: extension; module
   pair: C; language

Below is a list of the types that are built into Python.  Extension modules
(written in C, Java, or other languages, depending on the implementation) can
define additional types.  Future versions of Python may add types to the type
hierarchy (e.g., rational numbers, efficiently stored arrays of integers, etc.).

.. index::
   single: attribute
   pair: special; attribute
   triple: generic; special; attribute

Some of the type descriptions below contain a paragraph listing 'special
attributes.'  These are attributes that provide access to the implementation and
are not intended for general use.  Their definition may change in the future.

None
   .. index:: object: None

   This type has a single value.  There is a single object with this value. This
   object is accessed through the built-in name ``None``. It is used to signify the
   absence of a value in many situations, e.g., it is returned from functions that
   don't explicitly return anything. Its truth value is false.

NotImplemented
   .. index:: object: NotImplemented

   This type has a single value.  There is a single object with this value. This
   object is accessed through the built-in name ``NotImplemented``. Numeric methods
   and rich comparison methods may return this value if they do not implement the
   operation for the operands provided.  (The interpreter will then try the
   reflected operation, or some other fallback, depending on the operator.)  Its
   truth value is true.

Ellipsis
   .. index:: object: Ellipsis

   This type has a single value.  There is a single object with this value. This
   object is accessed through the built-in name ``Ellipsis``. It is used to
   indicate the presence of the ``...`` syntax in a slice.  Its truth value is
   true.

:class:`numbers.Number`
   .. index:: object: numeric

   These are created by numeric literals and returned as results by arithmetic
   operators and arithmetic built-in functions.  Numeric objects are immutable;
   once created their value never changes.  Python numbers are of course strongly
   related to mathematical numbers, but subject to the limitations of numerical
   representation in computers.

   Python distinguishes between integers, floating point numbers, and complex
   numbers:

   :class:`numbers.Integral`
      .. index:: object: integer

      These represent elements from the mathematical set of integers (positive and
      negative).

      There are three types of integers:

      Plain integers
         .. index::
            object: plain integer
            single: OverflowError (built-in exception)

         These represent numbers in the range -2147483648 through 2147483647.
         (The range may be larger on machines with a larger natural word size,
         but not smaller.)  When the result of an operation would fall outside
         this range, the result is normally returned as a long integer (in some
         cases, the exception :exc:`OverflowError` is raised instead).  For the
         purpose of shift and mask operations, integers are assumed to have a
         binary, 2's complement notation using 32 or more bits, and hiding no
         bits from the user (i.e., all 4294967296 different bit patterns
         correspond to different values).

      Long integers
         .. index:: object: long integer

         These represent numbers in an unlimited range, subject to available
         (virtual) memory only.  For the purpose of shift and mask operations, a
         binary representation is assumed, and negative numbers are represented
         in a variant of 2's complement which gives the illusion of an infinite
         string of sign bits extending to the left.

      Booleans
         .. index::
            object: Boolean
            single: False
            single: True

         These represent the truth values False and True.  The two objects
         representing the values ``False`` and ``True`` are the only Boolean objects.
         The Boolean type is a subtype of plain integers, and Boolean values
         behave like the values 0 and 1, respectively, in almost all contexts,
         the exception being that when converted to a string, the strings
         ``"False"`` or ``"True"`` are returned, respectively.

      .. index:: pair: integer; representation

      The rules for integer representation are intended to give the most
      meaningful interpretation of shift and mask operations involving negative
      integers and the least surprises when switching between the plain and long
      integer domains.  Any operation, if it yields a result in the plain
      integer domain, will yield the same result in the long integer domain or
      when using mixed operands.  The switch between domains is transparent to
      the programmer.

   :class:`numbers.Real` (:class:`float`)
      .. index::
         object: floating point
         pair: floating point; number
         pair: C; language
         pair: Java; language

      These represent machine-level double precision floating point numbers. You are
      at the mercy of the underlying machine architecture (and C or Java
      implementation) for the accepted range and handling of overflow. Python does not
      support single-precision floating point numbers; the savings in processor and
      memory usage that are usually the reason for using these are dwarfed by the
      overhead of using objects in Python, so there is no reason to complicate the
      language with two kinds of floating point numbers.

   :class:`numbers.Complex`
      .. index::
         object: complex
         pair: complex; number

      These represent complex numbers as a pair of machine-level double precision
      floating point numbers.  The same caveats apply as for floating point numbers.
      The real and imaginary parts of a complex number ``z`` can be retrieved through
      the read-only attributes ``z.real`` and ``z.imag``.

Sequences
   .. index::
      builtin: len
      object: sequence
      single: index operation
      single: item selection
      single: subscription

   These represent finite ordered sets indexed by non-negative numbers. The
   built-in function :func:`len` returns the number of items of a sequence. When
   the length of a sequence is *n*, the index set contains the numbers 0, 1,
   ..., *n*-1.  Item *i* of sequence *a* is selected by ``a[i]``.

   .. index:: single: slicing

   Sequences also support slicing: ``a[i:j]`` selects all items with index *k* such
   that *i* ``<=`` *k* ``<`` *j*.  When used as an expression, a slice is a
   sequence of the same type.  This implies that the index set is renumbered so
   that it starts at 0.

   .. index:: single: extended slicing

   Some sequences also support "extended slicing" with a third "step" parameter:
   ``a[i:j:k]`` selects all items of *a* with index *x* where ``x = i + n*k``, *n*
   ``>=`` ``0`` and *i* ``<=`` *x* ``<`` *j*.

   Sequences are distinguished according to their mutability:

   Immutable sequences
      .. index::
         object: immutable sequence
         object: immutable

      An object of an immutable sequence type cannot change once it is created.  (If
      the object contains references to other objects, these other objects may be
      mutable and may be changed; however, the collection of objects directly
      referenced by an immutable object cannot change.)

      The following types are immutable sequences:

      Strings
         .. index::
            builtin: chr
            builtin: ord
            object: string
            single: character
            single: byte
            single: ASCII@ASCII

         The items of a string are characters.  There is no separate character type; a
         character is represented by a string of one item. Characters represent (at
         least) 8-bit bytes.  The built-in functions :func:`chr` and :func:`ord` convert
         between characters and nonnegative integers representing the byte values.  Bytes
         with the values 0--127 usually represent the corresponding ASCII values, but the
         interpretation of values is up to the program.  The string data type is also
         used to represent arrays of bytes, e.g., to hold data read from a file.

         .. index::
            single: ASCII@ASCII
            single: EBCDIC
            single: character set
            pair: string; comparison
            builtin: chr
            builtin: ord

         (On systems whose native character set is not ASCII, strings may use EBCDIC in
         their internal representation, provided the functions :func:`chr` and
         :func:`ord` implement a mapping between ASCII and EBCDIC, and string comparison
         preserves the ASCII order. Or perhaps someone can propose a better rule?)

      Unicode
         .. index::
            builtin: unichr
            builtin: ord
            builtin: unicode
            object: unicode
            single: character
            single: integer
            single: Unicode

         The items of a Unicode object are Unicode code units.  A Unicode code unit is
         represented by a Unicode object of one item and can hold either a 16-bit or
         32-bit value representing a Unicode ordinal (the maximum value for the ordinal
         is given in ``sys.maxunicode``, and depends on how Python is configured at
         compile time).  Surrogate pairs may be present in the Unicode object, and will
         be reported as two separate items.  The built-in functions :func:`unichr` and
         :func:`ord` convert between code units and nonnegative integers representing the
         Unicode ordinals as defined in the Unicode Standard 3.0. Conversion from and to
         other encodings are possible through the Unicode method :meth:`encode` and the
         built-in function :func:`unicode`.

      Tuples
         .. index::
            object: tuple
            pair: singleton; tuple
            pair: empty; tuple

         The items of a tuple are arbitrary Python objects. Tuples of two or more items
         are formed by comma-separated lists of expressions.  A tuple of one item (a
         'singleton') can be formed by affixing a comma to an expression (an expression
         by itself does not create a tuple, since parentheses must be usable for grouping
         of expressions).  An empty tuple can be formed by an empty pair of parentheses.

   Mutable sequences
      .. index::
         object: mutable sequence
         object: mutable
         pair: assignment; statement
         single: subscription
         single: slicing

      Mutable sequences can be changed after they are created.  The subscription and
      slicing notations can be used as the target of assignment and :keyword:`del`
      (delete) statements.

      There are currently two intrinsic mutable sequence types:

      Lists
         .. index:: object: list

         The items of a list are arbitrary Python objects.  Lists are formed by placing a
         comma-separated list of expressions in square brackets. (Note that there are no
         special cases needed to form lists of length 0 or 1.)

      Byte Arrays
         .. index:: bytearray

         A bytearray object is a mutable array. They are created by the built-in
         :func:`bytearray` constructor.  Aside from being mutable (and hence
         unhashable), byte arrays otherwise provide the same interface and
         functionality as immutable bytes objects.

      .. index:: module: array

      The extension module :mod:`array` provides an additional example of a mutable
      sequence type.

Set types
   .. index::
      builtin: len
      object: set type

   These represent unordered, finite sets of unique, immutable objects. As such,
   they cannot be indexed by any subscript. However, they can be iterated over, and
   the built-in function :func:`len` returns the number of items in a set. Common
   uses for sets are fast membership testing, removing duplicates from a sequence,
   and computing mathematical operations such as intersection, union, difference,
   and symmetric difference.

   For set elements, the same immutability rules apply as for dictionary keys. Note
   that numeric types obey the normal rules for numeric comparison: if two numbers
   compare equal (e.g., ``1`` and ``1.0``), only one of them can be contained in a
   set.

   There are currently two intrinsic set types:

   Sets
      .. index:: object: set

      These represent a mutable set. They are created by the built-in :func:`set`
      constructor and can be modified afterwards by several methods, such as
      :meth:`~set.add`.

   Frozen sets
      .. index:: object: frozenset

      These represent an immutable set.  They are created by the built-in
      :func:`frozenset` constructor.  As a frozenset is immutable and
      :term:`hashable`, it can be used again as an element of another set, or as
      a dictionary key.

Mappings
   .. index::
      builtin: len
      single: subscription
      object: mapping

   These represent finite sets of objects indexed by arbitrary index sets. The
   subscript notation ``a[k]`` selects the item indexed by ``k`` from the mapping
   ``a``; this can be used in expressions and as the target of assignments or
   :keyword:`del` statements. The built-in function :func:`len` returns the number
   of items in a mapping.

   There is currently a single intrinsic mapping type:

   Dictionaries
      .. index:: object: dictionary

      These represent finite sets of objects indexed by nearly arbitrary values.  The
      only types of values not acceptable as keys are values containing lists or
      dictionaries or other mutable types that are compared by value rather than by
      object identity, the reason being that the efficient implementation of
      dictionaries requires a key's hash value to remain constant. Numeric types used
      for keys obey the normal rules for numeric comparison: if two numbers compare
      equal (e.g., ``1`` and ``1.0``) then they can be used interchangeably to index
      the same dictionary entry.

      Dictionaries are mutable; they can be created by the ``{...}`` notation (see
      section :ref:`dict`).

      .. index::
         module: dbm
         module: gdbm
         module: bsddb

      The extension modules :mod:`dbm`, :mod:`gdbm`, and :mod:`bsddb` provide
      additional examples of mapping types.

Callable types
   .. index::
      object: callable
      pair: function; call
      single: invocation
      pair: function; argument

   These are the types to which the function call operation (see section
   :ref:`calls`) can be applied:

   User-defined functions
      .. index::
         pair: user-defined; function
         object: function
         object: user-defined function

      A user-defined function object is created by a function definition (see
      section :ref:`function`).  It should be called with an argument list
      containing the same number of items as the function's formal parameter
      list.

      Special attributes:

      .. tabularcolumns:: |l|L|l|

      .. index::
         single: __doc__ (function attribute)
         single: __name__ (function attribute)
         single: __module__ (function attribute)
         single: __dict__ (function attribute)
         single: __defaults__ (function attribute)
         single: __code__ (function attribute)
         single: __globals__ (function attribute)
         single: __closure__ (function attribute)
         single: func_doc (function attribute)
         single: func_name (function attribute)
         single: func_dict (function attribute)
         single: func_defaults (function attribute)
         single: func_code (function attribute)
         single: func_globals (function attribute)
         single: func_closure (function attribute)
         pair: global; namespace

      +-----------------------+-------------------------------+-----------+
      | Attribute             | Meaning                       |           |
      +=======================+===============================+===========+
      | :attr:`__doc__`       | The function's documentation  | Writable  |
      | :attr:`func_doc`      | string, or ``None`` if        |           |
      |                       | unavailable.                  |           |
      +-----------------------+-------------------------------+-----------+
      | :attr:`~definition.\  | The function's name           | Writable  |
      | __name__`             |                               |           |
      | :attr:`func_name`     |                               |           |
      +-----------------------+-------------------------------+-----------+
      | :attr:`__module__`    | The name of the module the    | Writable  |
      |                       | function was defined in, or   |           |
      |                       | ``None`` if unavailable.      |           |
      +-----------------------+-------------------------------+-----------+
      | :attr:`__defaults__`  | A tuple containing default    | Writable  |
      | :attr:`func_defaults` | argument values for those     |           |
      |                       | arguments that have defaults, |           |
      |                       | or ``None`` if no arguments   |           |
      |                       | have a default value.         |           |
      +-----------------------+-------------------------------+-----------+
      | :attr:`__code__`      | The code object representing  | Writable  |
      | :attr:`func_code`     | the compiled function body.   |           |
      +-----------------------+-------------------------------+-----------+
      | :attr:`__globals__`   | A reference to the dictionary | Read-only |
      | :attr:`func_globals`  | that holds the function's     |           |
      |                       | global variables --- the      |           |
      |                       | global namespace of the       |           |
      |                       | module in which the function  |           |
      |                       | was defined.                  |           |
      +-----------------------+-------------------------------+-----------+
      | :attr:`~object.\      | The namespace supporting      | Writable  |
      | __dict__`             | arbitrary function            |           |
      | :attr:`func_dict`     | attributes.                   |           |
      +-----------------------+-------------------------------+-----------+
      | :attr:`__closure__`   | ``None`` or a tuple of cells  | Read-only |
      | :attr:`func_closure`  | that contain bindings for the |           |
      |                       | function's free variables.    |           |
      +-----------------------+-------------------------------+-----------+

      Most of the attributes labelled "Writable" check the type of the assigned value.

      .. versionchanged:: 2.4
         ``func_name`` is now writable.

      .. versionchanged:: 2.6
         The double-underscore attributes ``__closure__``, ``__code__``,
         ``__defaults__``, and ``__globals__`` were introduced as aliases for
         the corresponding ``func_*`` attributes for forwards compatibility
         with Python 3.

      Function objects also support getting and setting arbitrary attributes, which
      can be used, for example, to attach metadata to functions.  Regular attribute
      dot-notation is used to get and set such attributes. *Note that the current
      implementation only supports function attributes on user-defined functions.
      Function attributes on built-in functions may be supported in the future.*

      Additional information about a function's definition can be retrieved from its
      code object; see the description of internal types below.

   User-defined methods
      .. index::
         object: method
         object: user-defined method
         pair: user-defined; method

      A user-defined method object combines a class, a class instance (or ``None``)
      and any callable object (normally a user-defined function).

      Special read-only attributes: :attr:`im_self` is the class instance object,
      :attr:`im_func` is the function object; :attr:`im_class` is the class of
      :attr:`im_self` for bound methods or the class that asked for the method for
      unbound methods; :attr:`__doc__` is the method's documentation (same as
      ``im_func.__doc__``); :attr:`~definition.__name__` is the method name (same as
      ``im_func.__name__``); :attr:`__module__` is the name of the module the method
      was defined in, or ``None`` if unavailable.

      .. versionchanged:: 2.2
         :attr:`im_self` used to refer to the class that defined the method.

      .. versionchanged:: 2.6
         For Python 3 forward-compatibility, :attr:`im_func` is also available as
         :attr:`__func__`, and :attr:`im_self` as :attr:`__self__`.

      .. index::
         single: __doc__ (method attribute)
         single: __name__ (method attribute)
         single: __module__ (method attribute)
         single: im_func (method attribute)
         single: im_self (method attribute)

      Methods also support accessing (but not setting) the arbitrary function
      attributes on the underlying function object.

      User-defined method objects may be created when getting an attribute of a class
      (perhaps via an instance of that class), if that attribute is a user-defined
      function object, an unbound user-defined method object, or a class method
      object. When the attribute is a user-defined method object, a new method object
      is only created if the class from which it is being retrieved is the same as, or
      a derived class of, the class stored in the original method object; otherwise,
      the original method object is used as it is.

      .. index::
         single: im_class (method attribute)
         single: im_func (method attribute)
         single: im_self (method attribute)

      When a user-defined method object is created by retrieving a user-defined
      function object from a class, its :attr:`im_self` attribute is ``None``
      and the method object is said to be unbound. When one is created by
      retrieving a user-defined function object from a class via one of its
      instances, its :attr:`im_self` attribute is the instance, and the method
      object is said to be bound. In either case, the new method's
      :attr:`im_class` attribute is the class from which the retrieval takes
      place, and its :attr:`im_func` attribute is the original function object.

      .. index:: single: im_func (method attribute)

      When a user-defined method object is created by retrieving another method object
      from a class or instance, the behaviour is the same as for a function object,
      except that the :attr:`im_func` attribute of the new instance is not the
      original method object but its :attr:`im_func` attribute.

      .. index::
         single: im_class (method attribute)
         single: im_func (method attribute)
         single: im_self (method attribute)

      When a user-defined method object is created by retrieving a class method object
      from a class or instance, its :attr:`im_self` attribute is the class itself, and
      its :attr:`im_func` attribute is the function object underlying the class method.

      When an unbound user-defined method object is called, the underlying function
      (:attr:`im_func`) is called, with the restriction that the first argument must
      be an instance of the proper class (:attr:`im_class`) or of a derived class
      thereof.

      When a bound user-defined method object is called, the underlying function
      (:attr:`im_func`) is called, inserting the class instance (:attr:`im_self`) in
      front of the argument list.  For instance, when :class:`C` is a class which
      contains a definition for a function :meth:`f`, and ``x`` is an instance of
      :class:`C`, calling ``x.f(1)`` is equivalent to calling ``C.f(x, 1)``.

      When a user-defined method object is derived from a class method object, the
      "class instance" stored in :attr:`im_self` will actually be the class itself, so
      that calling either ``x.f(1)`` or ``C.f(1)`` is equivalent to calling ``f(C,1)``
      where ``f`` is the underlying function.

      Note that the transformation from function object to (unbound or bound) method
      object happens each time the attribute is retrieved from the class or instance.
      In some cases, a fruitful optimization is to assign the attribute to a local
      variable and call that local variable. Also notice that this transformation only
      happens for user-defined functions; other callable objects (and all non-callable
      objects) are retrieved without transformation.  It is also important to note
      that user-defined functions which are attributes of a class instance are not
      converted to bound methods; this *only* happens when the function is an
      attribute of the class.

   Generator functions
      .. index::
         single: generator; function
         single: generator; iterator

      A function or method which uses the :keyword:`yield` statement (see section
      :ref:`yield`) is called a :dfn:`generator
      function`.  Such a function, when called, always returns an iterator object
      which can be used to execute the body of the function:  calling the iterator's
      :meth:`~iterator.next` method will cause the function to execute until
      it provides a value
      using the :keyword:`yield` statement.  When the function executes a
      :keyword:`return` statement or falls off the end, a :exc:`StopIteration`
      exception is raised and the iterator will have reached the end of the set of
      values to be returned.

   Built-in functions
      .. index::
         object: built-in function
         object: function
         pair: C; language

      A built-in function object is a wrapper around a C function.  Examples of
      built-in functions are :func:`len` and :func:`math.sin` (:mod:`math` is a
      standard built-in module). The number and type of the arguments are
      determined by the C function. Special read-only attributes:
      :attr:`__doc__` is the function's documentation string, or ``None`` if
      unavailable; :attr:`~definition.__name__` is the function's name; :attr:`__self__` is
      set to ``None`` (but see the next item); :attr:`__module__` is the name of
      the module the function was defined in or ``None`` if unavailable.

   Built-in methods
      .. index::
         object: built-in method
         object: method
         pair: built-in; method

      This is really a different disguise of a built-in function, this time containing
      an object passed to the C function as an implicit extra argument.  An example of
      a built-in method is ``alist.append()``, assuming *alist* is a list object. In
      this case, the special read-only attribute :attr:`__self__` is set to the object
      denoted by *alist*.

   Class Types
      Class types, or "new-style classes," are callable.  These objects normally act
      as factories for new instances of themselves, but variations are possible for
      class types that override :meth:`__new__`.  The arguments of the call are passed
      to :meth:`__new__` and, in the typical case, to :meth:`__init__` to initialize
      the new instance.

   Classic Classes
      .. index::
         single: __init__() (object method)
         object: class
         object: class instance
         object: instance
         pair: class object; call

      Class objects are described below.  When a class object is called, a new class
      instance (also described below) is created and returned.  This implies a call to
      the class's :meth:`__init__` method if it has one.  Any arguments are passed on
      to the :meth:`__init__` method.  If there is no :meth:`__init__` method, the
      class must be called without arguments.

   Class instances
      Class instances are described below.  Class instances are callable only when the
      class has a :meth:`__call__` method; ``x(arguments)`` is a shorthand for
      ``x.__call__(arguments)``.

Modules
   .. index::
      statement: import
      object: module

   Modules are imported by the :keyword:`import` statement (see section
   :ref:`import`). A module object has a
   namespace implemented by a dictionary object (this is the dictionary referenced
   by the func_globals attribute of functions defined in the module).  Attribute
   references are translated to lookups in this dictionary, e.g., ``m.x`` is
   equivalent to ``m.__dict__["x"]``. A module object does not contain the code
   object used to initialize the module (since it isn't needed once the
   initialization is done).

   Attribute assignment updates the module's namespace dictionary, e.g., ``m.x =
   1`` is equivalent to ``m.__dict__["x"] = 1``.

   .. index:: single: __dict__ (module attribute)

   Special read-only attribute: :attr:`~object.__dict__` is the module's namespace as a
   dictionary object.

   .. impl-detail::

      Because of the way CPython clears module dictionaries, the module
      dictionary will be cleared when the module falls out of scope even if the
      dictionary still has live references.  To avoid this, copy the dictionary
      or keep the module around while using its dictionary directly.

   .. index::
      single: __name__ (module attribute)
      single: __doc__ (module attribute)
      single: __file__ (module attribute)
      pair: module; namespace

   Predefined (writable) attributes: :attr:`__name__` is the module's name;
   :attr:`__doc__` is the module's documentation string, or ``None`` if
   unavailable; :attr:`__file__` is the pathname of the file from which the module
   was loaded, if it was loaded from a file. The :attr:`__file__` attribute is not
   present for C modules that are statically linked into the interpreter; for
   extension modules loaded dynamically from a shared library, it is the pathname
   of the shared library file.

Classes
   Both class types (new-style classes) and class objects (old-style/classic
   classes) are typically created by class definitions (see section
   :ref:`class`).  A class has a namespace implemented by a dictionary object.
   Class attribute references are translated to lookups in this dictionary, e.g.,
   ``C.x`` is translated to ``C.__dict__["x"]`` (although for new-style classes
   in particular there are a number of hooks which allow for other means of
   locating attributes). When the attribute name is not found there, the
   attribute search continues in the base classes.  For old-style classes, the
   search is depth-first, left-to-right in the order of occurrence in the base
   class list. New-style classes use the more complex C3 method resolution
   order which behaves correctly even in the presence of 'diamond'
   inheritance structures where there are multiple inheritance paths
   leading back to a common ancestor. Additional details on the C3 MRO used by
   new-style classes can be found in the documentation accompanying the
   2.3 release at https://www.python.org/download/releases/2.3/mro/.

   .. XXX: Could we add that MRO doc as an appendix to the language ref?

   .. index::
      object: class
      object: class instance
      object: instance
      pair: class object; call
      single: container
      object: dictionary
      pair: class; attribute

   When a class attribute reference (for class :class:`C`, say) would yield a
   user-defined function object or an unbound user-defined method object whose
   associated class is either :class:`C` or one of its base classes, it is
   transformed into an unbound user-defined method object whose :attr:`im_class`
   attribute is :class:`C`. When it would yield a class method object, it is
   transformed into a bound user-defined method object whose
   :attr:`im_self` attribute is :class:`C`.  When it would yield a
   static method object, it is transformed into the object wrapped by the static
   method object. See section :ref:`descriptors` for another way in which
   attributes retrieved from a class may differ from those actually contained in
   its :attr:`~object.__dict__` (note that only new-style classes support descriptors).

   .. index:: triple: class; attribute; assignment

   Class attribute assignments update the class's dictionary, never the dictionary
   of a base class.

   .. index:: pair: class object; call

   A class object can be called (see above) to yield a class instance (see below).

   .. index::
      single: __name__ (class attribute)
      single: __module__ (class attribute)
      single: __dict__ (class attribute)
      single: __bases__ (class attribute)
      single: __doc__ (class attribute)

   Special attributes: :attr:`~definition.__name__` is the class name; :attr:`__module__` is
   the module name in which the class was defined; :attr:`~object.__dict__` is the
   dictionary containing the class's namespace; :attr:`~class.__bases__` is a
   tuple (possibly empty or a singleton) containing the base classes, in the
   order of their occurrence in the base class list; :attr:`__doc__` is the
   class's documentation string, or ``None`` if undefined.

Class instances
   .. index::
      object: class instance
      object: instance
      pair: class; instance
      pair: class instance; attribute

   A class instance is created by calling a class object (see above). A class
   instance has a namespace implemented as a dictionary which is the first place in
   which attribute references are searched.  When an attribute is not found there,
   and the instance's class has an attribute by that name, the search continues
   with the class attributes.  If a class attribute is found that is a user-defined
   function object or an unbound user-defined method object whose associated class
   is the class (call it :class:`C`) of the instance for which the attribute
   reference was initiated or one of its bases, it is transformed into a bound
   user-defined method object whose :attr:`im_class` attribute is :class:`C` and
   whose :attr:`im_self` attribute is the instance. Static method and class method
   objects are also transformed, as if they had been retrieved from class
   :class:`C`; see above under "Classes". See section :ref:`descriptors` for
   another way in which attributes of a class retrieved via its instances may
   differ from the objects actually stored in the class's :attr:`~object.__dict__`. If no
   class attribute is found, and the object's class has a :meth:`__getattr__`
   method, that is called to satisfy the lookup.

   .. index:: triple: class instance; attribute; assignment

   Attribute assignments and deletions update the instance's dictionary, never a
   class's dictionary.  If the class has a :meth:`__setattr__` or
   :meth:`__delattr__` method, this is called instead of updating the instance
   dictionary directly.

   .. index::
      object: numeric
      object: sequence
      object: mapping

   Class instances can pretend to be numbers, sequences, or mappings if they have
   methods with certain special names.  See section :ref:`specialnames`.

   .. index::
      single: __dict__ (instance attribute)
      single: __class__ (instance attribute)

   Special attributes: :attr:`~object.__dict__` is the attribute dictionary;
   :attr:`~instance.__class__` is the instance's class.

Files
   .. index::
      object: file
      builtin: open
      single: popen() (in module os)
      single: makefile() (socket method)
      single: sys.stdin
      single: sys.stdout
      single: sys.stderr
      single: stdio
      single: stdin (in module sys)
      single: stdout (in module sys)
      single: stderr (in module sys)

   A file object represents an open file.  File objects are created by the
   :func:`open` built-in function, and also by :func:`os.popen`,
   :func:`os.fdopen`, and the :meth:`makefile` method of socket objects (and
   perhaps by other functions or methods provided by extension modules).  The
   objects ``sys.stdin``, ``sys.stdout`` and ``sys.stderr`` are initialized to
   file objects corresponding to the interpreter's standard input, output and
   error streams.  See :ref:`bltin-file-objects` for complete documentation of
   file objects.

Internal types
   .. index::
      single: internal type
      single: types, internal

   A few types used internally by the interpreter are exposed to the user. Their
   definitions may change with future versions of the interpreter, but they are
   mentioned here for completeness.

   .. index:: bytecode, object; code, code object

   Code objects
      Code objects represent *byte-compiled* executable Python code, or :term:`bytecode`.
      The difference between a code object and a function object is that the function
      object contains an explicit reference to the function's globals (the module in
      which it was defined), while a code object contains no context; also the default
      argument values are stored in the function object, not in the code object
      (because they represent values calculated at run-time).  Unlike function
      objects, code objects are immutable and contain no references (directly or
      indirectly) to mutable objects.

      .. index::
         single: co_argcount (code object attribute)
         single: co_code (code object attribute)
         single: co_consts (code object attribute)
         single: co_filename (code object attribute)
         single: co_firstlineno (code object attribute)
         single: co_flags (code object attribute)
         single: co_lnotab (code object attribute)
         single: co_name (code object attribute)
         single: co_names (code object attribute)
         single: co_nlocals (code object attribute)
         single: co_stacksize (code object attribute)
         single: co_varnames (code object attribute)
         single: co_cellvars (code object attribute)
         single: co_freevars (code object attribute)

      Special read-only attributes: :attr:`co_name` gives the function name;
      :attr:`co_argcount` is the number of positional arguments (including arguments
      with default values); :attr:`co_nlocals` is the number of local variables used
      by the function (including arguments); :attr:`co_varnames` is a tuple containing
      the names of the local variables (starting with the argument names);
      :attr:`co_cellvars` is a tuple containing the names of local variables that are
      referenced by nested functions; :attr:`co_freevars` is a tuple containing the
      names of free variables; :attr:`co_code` is a string representing the sequence
      of bytecode instructions; :attr:`co_consts` is a tuple containing the literals
      used by the bytecode; :attr:`co_names` is a tuple containing the names used by
      the bytecode; :attr:`co_filename` is the filename from which the code was
      compiled; :attr:`co_firstlineno` is the first line number of the function;
      :attr:`co_lnotab` is a string encoding the mapping from bytecode offsets to
      line numbers (for details see the source code of the interpreter);
      :attr:`co_stacksize` is the required stack size (including local variables);
      :attr:`co_flags` is an integer encoding a number of flags for the interpreter.

      .. index:: object: generator

      The following flag bits are defined for :attr:`co_flags`: bit ``0x04`` is set if
      the function uses the ``*arguments`` syntax to accept an arbitrary number of
      positional arguments; bit ``0x08`` is set if the function uses the
      ``**keywords`` syntax to accept arbitrary keyword arguments; bit ``0x20`` is set
      if the function is a generator.

      Future feature declarations (``from __future__ import division``) also use bits
      in :attr:`co_flags` to indicate whether a code object was compiled with a
      particular feature enabled: bit ``0x2000`` is set if the function was compiled
      with future division enabled; bits ``0x10`` and ``0x1000`` were used in earlier
      versions of Python.

      Other bits in :attr:`co_flags` are reserved for internal use.

      .. index:: single: documentation string

      If a code object represents a function, the first item in :attr:`co_consts` is
      the documentation string of the function, or ``None`` if undefined.

   .. _frame-objects:

   Frame objects
      .. index:: object: frame

      Frame objects represent execution frames.  They may occur in traceback objects
      (see below).

      .. index::
         single: f_back (frame attribute)
         single: f_code (frame attribute)
         single: f_globals (frame attribute)
         single: f_locals (frame attribute)
         single: f_lasti (frame attribute)
         single: f_builtins (frame attribute)
         single: f_restricted (frame attribute)

      Special read-only attributes: :attr:`f_back` is to the previous stack frame
      (towards the caller), or ``None`` if this is the bottom stack frame;
      :attr:`f_code` is the code object being executed in this frame; :attr:`f_locals`
      is the dictionary used to look up local variables; :attr:`f_globals` is used for
      global variables; :attr:`f_builtins` is used for built-in (intrinsic) names;
      :attr:`f_restricted` is a flag indicating whether the function is executing in
      restricted execution mode; :attr:`f_lasti` gives the precise instruction (this
      is an index into the bytecode string of the code object).

      .. index::
         single: f_trace (frame attribute)
         single: f_exc_type (frame attribute)
         single: f_exc_value (frame attribute)
         single: f_exc_traceback (frame attribute)
         single: f_lineno (frame attribute)

      Special writable attributes: :attr:`f_trace`, if not ``None``, is a function
      called at the start of each source code line (this is used by the debugger);
      :attr:`f_exc_type`, :attr:`f_exc_value`, :attr:`f_exc_traceback` represent the
      last exception raised in the parent frame provided another exception was ever
      raised in the current frame (in all other cases they are ``None``); :attr:`f_lineno`
      is the current line number of the frame --- writing to this from within a trace
      function jumps to the given line (only for the bottom-most frame).  A debugger
      can implement a Jump command (aka Set Next Statement) by writing to f_lineno.

   Traceback objects
      .. index::
         object: traceback
         pair: stack; trace
         pair: exception; handler
         pair: execution; stack
         single: exc_info (in module sys)
         single: exc_traceback (in module sys)
         single: last_traceback (in module sys)
         single: sys.exc_info
         single: sys.exc_traceback
         single: sys.last_traceback

      Traceback objects represent a stack trace of an exception.  A traceback object
      is created when an exception occurs.  When the search for an exception handler
      unwinds the execution stack, at each unwound level a traceback object is
      inserted in front of the current traceback.  When an exception handler is
      entered, the stack trace is made available to the program. (See section
      :ref:`try`.) It is accessible as ``sys.exc_traceback``,
      and also as the third item of the tuple returned by ``sys.exc_info()``.  The
      latter is the preferred interface, since it works correctly when the program is
      using multiple threads. When the program contains no suitable handler, the stack
      trace is written (nicely formatted) to the standard error stream; if the
      interpreter is interactive, it is also made available to the user as
      ``sys.last_traceback``.

      .. index::
         single: tb_next (traceback attribute)
         single: tb_frame (traceback attribute)
         single: tb_lineno (traceback attribute)
         single: tb_lasti (traceback attribute)
         statement: try

      Special read-only attributes: :attr:`tb_next` is the next level in the stack
      trace (towards the frame where the exception occurred), or ``None`` if there is
      no next level; :attr:`tb_frame` points to the execution frame of the current
      level; :attr:`tb_lineno` gives the line number where the exception occurred;
      :attr:`tb_lasti` indicates the precise instruction.  The line number and last
      instruction in the traceback may differ from the line number of its frame object
      if the exception occurred in a :keyword:`try` statement with no matching except
      clause or with a finally clause.

   Slice objects
      .. index:: builtin: slice

      Slice objects are used to represent slices when *extended slice syntax* is used.
      This is a slice using two colons, or multiple slices or ellipses separated by
      commas, e.g., ``a[i:j:step]``, ``a[i:j, k:l]``, or ``a[..., i:j]``.  They are
      also created by the built-in :func:`slice` function.

      .. index::
         single: start (slice object attribute)
         single: stop (slice object attribute)
         single: step (slice object attribute)

      Special read-only attributes: :attr:`~slice.start` is the lower bound;
      :attr:`~slice.stop` is the upper bound; :attr:`~slice.step` is the step
      value; each is ``None`` if omitted.  These attributes can have any type.

      Slice objects support one method:


      .. method:: slice.indices(self, length)

         This method takes a single integer argument *length* and computes information
         about the extended slice that the slice object would describe if applied to a
         sequence of *length* items.  It returns a tuple of three integers; respectively
         these are the *start* and *stop* indices and the *step* or stride length of the
         slice. Missing or out-of-bounds indices are handled in a manner consistent with
         regular slices.

         .. versionadded:: 2.3

   Static method objects
      Static method objects provide a way of defeating the transformation of function
      objects to method objects described above. A static method object is a wrapper
      around any other object, usually a user-defined method object. When a static
      method object is retrieved from a class or a class instance, the object actually
      returned is the wrapped object, which is not subject to any further
      transformation. Static method objects are not themselves callable, although the
      objects they wrap usually are. Static method objects are created by the built-in
      :func:`staticmethod` constructor.

   Class method objects
      A class method object, like a static method object, is a wrapper around another
      object that alters the way in which that object is retrieved from classes and
      class instances. The behaviour of class method objects upon such retrieval is
      described above, under "User-defined methods". Class method objects are created
      by the built-in :func:`classmethod` constructor.


.. _newstyle:

New-style and classic classes
=============================

Classes and instances come in two flavors: old-style (or classic) and new-style.

Up to Python 2.1 the concept of ``class`` was unrelated to the concept of
``type``, and old-style classes were the only flavor available.  For an
old-style class, the statement ``x.__class__`` provides the class of *x*, but
``type(x)`` is always ``<type 'instance'>``.  This reflects the fact that all
old-style instances, independent of their class, are implemented with a single
built-in type, called ``instance``.

New-style classes were introduced in Python 2.2 to unify the concepts of
``class`` and ``type``.  A new-style class is simply a user-defined type,
no more, no less.  If *x* is an instance of a new-style class, then ``type(x)``
is typically the same as ``x.__class__`` (although this is not guaranteed -- a
new-style class instance is permitted to override the value returned for
``x.__class__``).

The major motivation for introducing new-style classes is to provide a unified
object model with a full meta-model.  It also has a number of practical
benefits, like the ability to subclass most built-in types, or the introduction
of "descriptors", which enable computed properties.

For compatibility reasons, classes are still old-style by default.  New-style
classes are created by specifying another new-style class (i.e. a type) as a
parent class, or the "top-level type" :class:`object` if no other parent is
needed.  The behaviour of new-style classes differs from that of old-style
classes in a number of important details in addition to what :func:`type`
returns.  Some of these changes are fundamental to the new object model, like
the way special methods are invoked.  Others are "fixes" that could not be
implemented before for compatibility concerns, like the method resolution order
in case of multiple inheritance.

While this manual aims to provide comprehensive coverage of Python's class
mechanics, it may still be lacking in some areas when it comes to its coverage
of new-style classes. Please see https://www.python.org/doc/newstyle/ for
sources of additional information.

.. index::
   single: class; new-style
   single: class; classic
   single: class; old-style

Old-style classes are removed in Python 3, leaving only new-style classes.


.. _specialnames:

Special method names
====================

.. index::
   pair: operator; overloading
   single: __getitem__() (mapping object method)

A class can implement certain operations that are invoked by special syntax
(such as arithmetic operations or subscripting and slicing) by defining methods
with special names. This is Python's approach to :dfn:`operator overloading`,
allowing classes to define their own behavior with respect to language
operators.  For instance, if a class defines a method named :meth:`__getitem__`,
and ``x`` is an instance of this class, then ``x[i]`` is roughly equivalent
to ``x.__getitem__(i)`` for old-style classes and ``type(x).__getitem__(x, i)``
for new-style classes.  Except where mentioned, attempts to execute an
operation raise an exception when no appropriate method is defined (typically
:exc:`AttributeError` or :exc:`TypeError`).

When implementing a class that emulates any built-in type, it is important that
the emulation only be implemented to the degree that it makes sense for the
object being modelled.  For example, some sequences may work well with retrieval
of individual elements, but extracting a slice may not make sense.  (One example
of this is the :class:`~xml.dom.NodeList` interface in the W3C's Document
Object Model.)


.. _customization:

Basic customization
-------------------

.. method:: object.__new__(cls[, ...])

   .. index:: pair: subclassing; immutable types

   Called to create a new instance of class *cls*.  :meth:`__new__` is a static
   method (special-cased so you need not declare it as such) that takes the class
   of which an instance was requested as its first argument.  The remaining
   arguments are those passed to the object constructor expression (the call to the
   class).  The return value of :meth:`__new__` should be the new object instance
   (usually an instance of *cls*).

   Typical implementations create a new instance of the class by invoking the
   superclass's :meth:`__new__` method using ``super(currentclass,
   cls).__new__(cls[, ...])`` with appropriate arguments and then modifying the
   newly-created instance as necessary before returning it.

   If :meth:`__new__` returns an instance of *cls*, then the new instance's
   :meth:`__init__` method will be invoked like ``__init__(self[, ...])``, where
   *self* is the new instance and the remaining arguments are the same as were
   passed to :meth:`__new__`.

   If :meth:`__new__` does not return an instance of *cls*, then the new instance's
   :meth:`__init__` method will not be invoked.

   :meth:`__new__` is intended mainly to allow subclasses of immutable types (like
   int, str, or tuple) to customize instance creation.  It is also commonly
   overridden in custom metaclasses in order to customize class creation.


.. method:: object.__init__(self[, ...])

   .. index:: pair: class; constructor

   Called after the instance has been created (by :meth:`__new__`), but before
   it is returned to the caller.  The arguments are those passed to the
   class constructor expression.  If a base class has an :meth:`__init__` method,
   the derived class's :meth:`__init__` method, if any, must explicitly call it to
   ensure proper initialization of the base class part of the instance; for
   example: ``BaseClass.__init__(self, [args...])``.

   Because :meth:`__new__` and :meth:`__init__` work together in constructing
   objects (:meth:`__new__` to create it, and :meth:`__init__` to customise it),
   no non-``None`` value may be returned by :meth:`__init__`; doing so will
   cause a :exc:`TypeError` to be raised at runtime.


.. method:: object.__del__(self)

   .. index::
      single: destructor
      statement: del

   Called when the instance is about to be destroyed.  This is also called a
   destructor.  If a base class has a :meth:`__del__` method, the derived class's
   :meth:`__del__` method, if any, must explicitly call it to ensure proper
   deletion of the base class part of the instance.  Note that it is possible
   (though not recommended!) for the :meth:`__del__` method to postpone destruction
   of the instance by creating a new reference to it.  It may then be called at a
   later time when this new reference is deleted.  It is not guaranteed that
   :meth:`__del__` methods are called for objects that still exist when the
   interpreter exits.

   .. note::

      ``del x`` doesn't directly call ``x.__del__()`` --- the former decrements
      the reference count for ``x`` by one, and the latter is only called when
      ``x``'s reference count reaches zero.  Some common situations that may
      prevent the reference count of an object from going to zero include:
      circular references between objects (e.g., a doubly-linked list or a tree
      data structure with parent and child pointers); a reference to the object
      on the stack frame of a function that caught an exception (the traceback
      stored in ``sys.exc_traceback`` keeps the stack frame alive); or a
      reference to the object on the stack frame that raised an unhandled
      exception in interactive mode (the traceback stored in
      ``sys.last_traceback`` keeps the stack frame alive).  The first situation
      can only be remedied by explicitly breaking the cycles; the latter two
      situations can be resolved by storing ``None`` in ``sys.exc_traceback`` or
      ``sys.last_traceback``.  Circular references which are garbage are
      detected when the option cycle detector is enabled (it's on by default),
      but can only be cleaned up if there are no Python-level :meth:`__del__`
      methods involved. Refer to the documentation for the :mod:`gc` module for
      more information about how :meth:`__del__` methods are handled by the
      cycle detector, particularly the description of the ``garbage`` value.

   .. warning::

      Due to the precarious circumstances under which :meth:`__del__` methods are
      invoked, exceptions that occur during their execution are ignored, and a warning
      is printed to ``sys.stderr`` instead.  Also, when :meth:`__del__` is invoked in
      response to a module being deleted (e.g., when execution of the program is
      done), other globals referenced by the :meth:`__del__` method may already have
      been deleted or in the process of being torn down (e.g. the import
      machinery shutting down).  For this reason, :meth:`__del__` methods
      should do the absolute
      minimum needed to maintain external invariants.  Starting with version 1.5,
      Python guarantees that globals whose name begins with a single underscore are
      deleted from their module before other globals are deleted; if no other
      references to such globals exist, this may help in assuring that imported
      modules are still available at the time when the :meth:`__del__` method is
      called.

   See also the :option:`-R` command-line option.


.. method:: object.__repr__(self)

   .. index:: builtin: repr

   Called by the :func:`repr` built-in function and by string conversions (reverse
   quotes) to compute the "official" string representation of an object.  If at all
   possible, this should look like a valid Python expression that could be used to
   recreate an object with the same value (given an appropriate environment).  If
   this is not possible, a string of the form ``<...some useful description...>``
   should be returned.  The return value must be a string object. If a class
   defines :meth:`__repr__` but not :meth:`__str__`, then :meth:`__repr__` is also
   used when an "informal" string representation of instances of that class is
   required.

   .. index::
      pair: string; conversion
      pair: reverse; quotes
      pair: backward; quotes
      single: back-quotes

   This is typically used for debugging, so it is important that the representation
   is information-rich and unambiguous.


.. method:: object.__str__(self)

   .. index::
      builtin: str
      statement: print

   Called by the :func:`str` built-in function and by the :keyword:`print`
   statement to compute the "informal" string representation of an object.  This
   differs from :meth:`__repr__` in that it does not have to be a valid Python
   expression: a more convenient or concise representation may be used instead.
   The return value must be a string object.


.. method:: object.__lt__(self, other)
            object.__le__(self, other)
            object.__eq__(self, other)
            object.__ne__(self, other)
            object.__gt__(self, other)
            object.__ge__(self, other)

   .. versionadded:: 2.1

   .. index::
      single: comparisons

   These are the so-called "rich comparison" methods, and are called for comparison
   operators in preference to :meth:`__cmp__` below. The correspondence between
   operator symbols and method names is as follows: ``x<y`` calls ``x.__lt__(y)``,
   ``x<=y`` calls ``x.__le__(y)``, ``x==y`` calls ``x.__eq__(y)``, ``x!=y`` and
   ``x<>y`` call ``x.__ne__(y)``, ``x>y`` calls ``x.__gt__(y)``, and ``x>=y`` calls
   ``x.__ge__(y)``.

   A rich comparison method may return the singleton ``NotImplemented`` if it does
   not implement the operation for a given pair of arguments. By convention,
   ``False`` and ``True`` are returned for a successful comparison. However, these
   methods can return any value, so if the comparison operator is used in a Boolean
   context (e.g., in the condition of an ``if`` statement), Python will call
   :func:`bool` on the value to determine if the result is true or false.

   There are no implied relationships among the comparison operators. The truth
   of ``x==y`` does not imply that ``x!=y`` is false.  Accordingly, when
   defining :meth:`__eq__`, one should also define :meth:`__ne__` so that the
   operators will behave as expected.  See the paragraph on :meth:`__hash__` for
   some important notes on creating :term:`hashable` objects which support
   custom comparison operations and are usable as dictionary keys.

   There are no swapped-argument versions of these methods (to be used when the
   left argument does not support the operation but the right argument does);
   rather, :meth:`__lt__` and :meth:`__gt__` are each other's reflection,
   :meth:`__le__` and :meth:`__ge__` are each other's reflection, and
   :meth:`__eq__` and :meth:`__ne__` are their own reflection.

   Arguments to rich comparison methods are never coerced.

   To automatically generate ordering operations from a single root operation,
   see :func:`functools.total_ordering`.

.. method:: object.__cmp__(self, other)

   .. index::
      builtin: cmp
      single: comparisons

   Called by comparison operations if rich comparison (see above) is not
   defined.  Should return a negative integer if ``self < other``, zero if
   ``self == other``, a positive integer if ``self > other``.  If no
   :meth:`__cmp__`, :meth:`__eq__` or :meth:`__ne__` operation is defined, class
   instances are compared by object identity ("address").  See also the
   description of :meth:`__hash__` for some important notes on creating
   :term:`hashable` objects which support custom comparison operations and are
   usable as dictionary keys. (Note: the restriction that exceptions are not
   propagated by :meth:`__cmp__` has been removed since Python 1.5.)


.. method:: object.__rcmp__(self, other)

   .. versionchanged:: 2.1
      No longer supported.


.. method:: object.__hash__(self)

   .. index::
      object: dictionary
      builtin: hash

   Called by built-in function :func:`hash` and for operations on members of
   hashed collections including :class:`set`, :class:`frozenset`, and
   :class:`dict`.  :meth:`__hash__` should return an integer.  The only required
   property is that objects which compare equal have the same hash value; it is
   advised to mix together the hash values of the components of the object that
   also play a part in comparison of objects by packing them into a tuple and
   hashing the tuple. Example::

       def __hash__(self):
           return hash((self.name, self.nick, self.color))

   If a class does not define a :meth:`__cmp__` or :meth:`__eq__` method it
   should not define a :meth:`__hash__` operation either; if it defines
   :meth:`__cmp__` or :meth:`__eq__` but not :meth:`__hash__`, its instances
   will not be usable in hashed collections.  If a class defines mutable objects
   and implements a :meth:`__cmp__` or :meth:`__eq__` method, it should not
   implement :meth:`__hash__`, since hashable collection implementations require
   that an object's hash value is immutable (if the object's hash value changes,
   it will be in the wrong hash bucket).

   User-defined classes have :meth:`__cmp__` and :meth:`__hash__` methods
   by default; with them, all objects compare unequal (except with themselves)
   and ``x.__hash__()`` returns a result derived from ``id(x)``.

   Classes which inherit a :meth:`__hash__` method from a parent class but
   change the meaning of :meth:`__cmp__` or :meth:`__eq__` such that the hash
   value returned is no longer appropriate (e.g. by switching to a value-based
   concept of equality instead of the default identity based equality) can
   explicitly flag themselves as being unhashable by setting ``__hash__ = None``
   in the class definition. Doing so means that not only will instances of the
   class raise an appropriate :exc:`TypeError` when a program attempts to
   retrieve their hash value, but they will also be correctly identified as
   unhashable when checking ``isinstance(obj, collections.Hashable)`` (unlike
   classes which define their own :meth:`__hash__` to explicitly raise
   :exc:`TypeError`).

   .. versionchanged:: 2.5
      :meth:`__hash__` may now also return a long integer object; the 32-bit
      integer is then derived from the hash of that object.

   .. versionchanged:: 2.6
      :attr:`__hash__` may now be set to :const:`None` to explicitly flag
      instances of a class as unhashable.


.. method:: object.__nonzero__(self)

   .. index:: single: __len__() (mapping object method)

   Called to implement truth value testing and the built-in operation ``bool()``;
   should return ``False`` or ``True``, or their integer equivalents ``0`` or
   ``1``.  When this method is not defined, :meth:`__len__` is called, if it is
   defined, and the object is considered true if its result is nonzero.
   If a class defines neither :meth:`__len__` nor :meth:`__nonzero__`, all its
   instances are considered true.


.. method:: object.__unicode__(self)

   .. index:: builtin: unicode

   Called to implement :func:`unicode` built-in; should return a Unicode object.
   When this method is not defined, string conversion is attempted, and the result
   of string conversion is converted to Unicode using the system default encoding.


.. _attribute-access:

Customizing attribute access
----------------------------

The following methods can be defined to customize the meaning of attribute
access (use of, assignment to, or deletion of ``x.name``) for class instances.


.. method:: object.__getattr__(self, name)

   Called when an attribute lookup has not found the attribute in the usual places
   (i.e. it is not an instance attribute nor is it found in the class tree for
   ``self``).  ``name`` is the attribute name. This method should return the
   (computed) attribute value or raise an :exc:`AttributeError` exception.

   .. index:: single: __setattr__() (object method)

   Note that if the attribute is found through the normal mechanism,
   :meth:`__getattr__` is not called.  (This is an intentional asymmetry between
   :meth:`__getattr__` and :meth:`__setattr__`.) This is done both for efficiency
   reasons and because otherwise :meth:`__getattr__` would have no way to access
   other attributes of the instance.  Note that at least for instance variables,
   you can fake total control by not inserting any values in the instance attribute
   dictionary (but instead inserting them in another object).  See the
   :meth:`__getattribute__` method below for a way to actually get total control in
   new-style classes.


.. method:: object.__setattr__(self, name, value)

   Called when an attribute assignment is attempted.  This is called instead of the
   normal mechanism (i.e. store the value in the instance dictionary).  *name* is
   the attribute name, *value* is the value to be assigned to it.

   .. index:: single: __dict__ (instance attribute)

   If :meth:`__setattr__` wants to assign to an instance attribute, it should not
   simply execute ``self.name = value`` --- this would cause a recursive call to
   itself.  Instead, it should insert the value in the dictionary of instance
   attributes, e.g., ``self.__dict__[name] = value``.  For new-style classes,
   rather than accessing the instance dictionary, it should call the base class
   method with the same name, for example, ``object.__setattr__(self, name,
   value)``.


.. method:: object.__delattr__(self, name)

   Like :meth:`__setattr__` but for attribute deletion instead of assignment.  This
   should only be implemented if ``del obj.name`` is meaningful for the object.


.. _new-style-attribute-access:

More attribute access for new-style classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following methods only apply to new-style classes.


.. method:: object.__getattribute__(self, name)

   Called unconditionally to implement attribute accesses for instances of the
   class. If the class also defines :meth:`__getattr__`, the latter will not be
   called unless :meth:`__getattribute__` either calls it explicitly or raises an
   :exc:`AttributeError`. This method should return the (computed) attribute value
   or raise an :exc:`AttributeError` exception. In order to avoid infinite
   recursion in this method, its implementation should always call the base class
   method with the same name to access any attributes it needs, for example,
   ``object.__getattribute__(self, name)``.

   .. note::

      This method may still be bypassed when looking up special methods as the
      result of implicit invocation via language syntax or built-in functions.
      See :ref:`new-style-special-lookup`.


.. _descriptors:

Implementing Descriptors
^^^^^^^^^^^^^^^^^^^^^^^^

The following methods only apply when an instance of the class containing the
method (a so-called *descriptor* class) appears in an *owner* class (the
descriptor must be in either the owner's class dictionary or in the class
dictionary for one of its parents).  In the examples below, "the attribute"
refers to the attribute whose name is the key of the property in the owner
class' :attr:`~object.__dict__`.


.. method:: object.__get__(self, instance, owner)

   Called to get the attribute of the owner class (class attribute access) or of an
   instance of that class (instance attribute access). *owner* is always the owner
   class, while *instance* is the instance that the attribute was accessed through,
   or ``None`` when the attribute is accessed through the *owner*.  This method
   should return the (computed) attribute value or raise an :exc:`AttributeError`
   exception.


.. method:: object.__set__(self, instance, value)

   Called to set the attribute on an instance *instance* of the owner class to a
   new value, *value*.


.. method:: object.__delete__(self, instance)

   Called to delete the attribute on an instance *instance* of the owner class.


.. _descriptor-invocation:

Invoking Descriptors
^^^^^^^^^^^^^^^^^^^^

In general, a descriptor is an object attribute with "binding behavior", one
whose attribute access has been overridden by methods in the descriptor
protocol:  :meth:`__get__`, :meth:`__set__`, and :meth:`__delete__`. If any of
those methods are defined for an object, it is said to be a descriptor.

The default behavior for attribute access is to get, set, or delete the
attribute from an object's dictionary. For instance, ``a.x`` has a lookup chain
starting with ``a.__dict__['x']``, then ``type(a).__dict__['x']``, and
continuing through the base classes of ``type(a)`` excluding metaclasses.

However, if the looked-up value is an object defining one of the descriptor
methods, then Python may override the default behavior and invoke the descriptor
method instead.  Where this occurs in the precedence chain depends on which
descriptor methods were defined and how they were called.  Note that descriptors
are only invoked for new style objects or classes (ones that subclass
:class:`object()` or :class:`type()`).

The starting point for descriptor invocation is a binding, ``a.x``. How the
arguments are assembled depends on ``a``:

Direct Call
   The simplest and least common call is when user code directly invokes a
   descriptor method:    ``x.__get__(a)``.

Instance Binding
   If binding to a new-style object instance, ``a.x`` is transformed into the call:
   ``type(a).__dict__['x'].__get__(a, type(a))``.

Class Binding
   If binding to a new-style class, ``A.x`` is transformed into the call:
   ``A.__dict__['x'].__get__(None, A)``.

Super Binding
   If ``a`` is an instance of :class:`super`, then the binding ``super(B,
   obj).m()`` searches ``obj.__class__.__mro__`` for the base class ``A``
   immediately preceding ``B`` and then invokes the descriptor with the call:
   ``A.__dict__['m'].__get__(obj, obj.__class__)``.

For instance bindings, the precedence of descriptor invocation depends on the
which descriptor methods are defined.  A descriptor can define any combination
of :meth:`__get__`, :meth:`__set__` and :meth:`__delete__`.  If it does not
define :meth:`__get__`, then accessing the attribute will return the descriptor
object itself unless there is a value in the object's instance dictionary.  If
the descriptor defines :meth:`__set__` and/or :meth:`__delete__`, it is a data
descriptor; if it defines neither, it is a non-data descriptor.  Normally, data
descriptors define both :meth:`__get__` and :meth:`__set__`, while non-data
descriptors have just the :meth:`__get__` method.  Data descriptors with
:meth:`__set__` and :meth:`__get__` defined always override a redefinition in an
instance dictionary.  In contrast, non-data descriptors can be overridden by
instances.

Python methods (including :func:`staticmethod` and :func:`classmethod`) are
implemented as non-data descriptors.  Accordingly, instances can redefine and
override methods.  This allows individual instances to acquire behaviors that
differ from other instances of the same class.

The :func:`property` function is implemented as a data descriptor. Accordingly,
instances cannot override the behavior of a property.


.. _slots:

__slots__
^^^^^^^^^

By default, instances of both old and new-style classes have a dictionary for
attribute storage.  This wastes space for objects having very few instance
variables.  The space consumption can become acute when creating large numbers
of instances.

The default can be overridden by defining *__slots__* in a new-style class
definition.  The *__slots__* declaration takes a sequence of instance variables
and reserves just enough space in each instance to hold a value for each
variable.  Space is saved because *__dict__* is not created for each instance.


.. data:: __slots__

   This class variable can be assigned a string, iterable, or sequence of strings
   with variable names used by instances.  If defined in a new-style class,
   *__slots__* reserves space for the declared variables and prevents the automatic
   creation of *__dict__* and *__weakref__* for each instance.

   .. versionadded:: 2.2

Notes on using *__slots__*

* When inheriting from a class without *__slots__*, the *__dict__* attribute of
  that class will always be accessible, so a *__slots__* definition in the
  subclass is meaningless.

* Without a *__dict__* variable, instances cannot be assigned new variables not
  listed in the *__slots__* definition.  Attempts to assign to an unlisted
  variable name raises :exc:`AttributeError`. If dynamic assignment of new
  variables is desired, then add ``'__dict__'`` to the sequence of strings in the
  *__slots__* declaration.

  .. versionchanged:: 2.3
     Previously, adding ``'__dict__'`` to the *__slots__* declaration would not
     enable the assignment of new attributes not specifically listed in the sequence
     of instance variable names.

* Without a *__weakref__* variable for each instance, classes defining
  *__slots__* do not support weak references to its instances. If weak reference
  support is needed, then add ``'__weakref__'`` to the sequence of strings in the
  *__slots__* declaration.

  .. versionchanged:: 2.3
     Previously, adding ``'__weakref__'`` to the *__slots__* declaration would not
     enable support for weak references.

* *__slots__* are implemented at the class level by creating descriptors
  (:ref:`descriptors`) for each variable name.  As a result, class attributes
  cannot be used to set default values for instance variables defined by
  *__slots__*; otherwise, the class attribute would overwrite the descriptor
  assignment.

* The action of a *__slots__* declaration is limited to the class where it is
  defined.  As a result, subclasses will have a *__dict__* unless they also define
  *__slots__* (which must only contain names of any *additional* slots).

* If a class defines a slot also defined in a base class, the instance variable
  defined by the base class slot is inaccessible (except by retrieving its
  descriptor directly from the base class). This renders the meaning of the
  program undefined.  In the future, a check may be added to prevent this.

* Nonempty *__slots__* does not work for classes derived from "variable-length"
  built-in types such as :class:`long`, :class:`str` and :class:`tuple`.

* Any non-string iterable may be assigned to *__slots__*. Mappings may also be
  used; however, in the future, special meaning may be assigned to the values
  corresponding to each key.

* *__class__* assignment works only if both classes have the same *__slots__*.

  .. versionchanged:: 2.6
     Previously, *__class__* assignment raised an error if either new or old class
     had *__slots__*.


.. _metaclasses:

Customizing class creation
--------------------------

By default, new-style classes are constructed using :func:`type`. A class
definition is read into a separate namespace and the value of class name is
bound to the result of ``type(name, bases, dict)``.

When the class definition is read, if *__metaclass__* is defined then the
callable assigned to it will be called instead of :func:`type`. This allows
classes or functions to be written which monitor or alter the class creation
process:

* Modifying the class dictionary prior to the class being created.

* Returning an instance of another class -- essentially performing the role of a
  factory function.

These steps will have to be performed in the metaclass's :meth:`__new__` method
-- :meth:`type.__new__` can then be called from this method to create a class
with different properties.  This example adds a new element to the class
dictionary before creating the class::

  class metacls(type):
      def __new__(mcs, name, bases, dict):
          dict['foo'] = 'metacls was here'
          return type.__new__(mcs, name, bases, dict)

You can of course also override other class methods (or add new methods); for
example defining a custom :meth:`__call__` method in the metaclass allows custom
behavior when the class is called, e.g. not always creating a new instance.


.. data:: __metaclass__

   This variable can be any callable accepting arguments for ``name``, ``bases``,
   and ``dict``.  Upon class creation, the callable is used instead of the built-in
   :func:`type`.

   .. versionadded:: 2.2

The appropriate metaclass is determined by the following precedence rules:

* If ``dict['__metaclass__']`` exists, it is used.

* Otherwise, if there is at least one base class, its metaclass is used (this
  looks for a *__class__* attribute first and if not found, uses its type).

* Otherwise, if a global variable named __metaclass__ exists, it is used.

* Otherwise, the old-style, classic metaclass (types.ClassType) is used.

The potential uses for metaclasses are boundless. Some ideas that have been
explored including logging, interface checking, automatic delegation, automatic
property creation, proxies, frameworks, and automatic resource
locking/synchronization.


Customizing instance and subclass checks
----------------------------------------

.. versionadded:: 2.6

The following methods are used to override the default behavior of the
:func:`isinstance` and :func:`issubclass` built-in functions.

In particular, the metaclass :class:`abc.ABCMeta` implements these methods in
order to allow the addition of Abstract Base Classes (ABCs) as "virtual base
classes" to any class or type (including built-in types), including other
ABCs.

.. method:: class.__instancecheck__(self, instance)

   Return true if *instance* should be considered a (direct or indirect)
   instance of *class*. If defined, called to implement ``isinstance(instance,
   class)``.


.. method:: class.__subclasscheck__(self, subclass)

   Return true if *subclass* should be considered a (direct or indirect)
   subclass of *class*.  If defined, called to implement ``issubclass(subclass,
   class)``.


Note that these methods are looked up on the type (metaclass) of a class.  They
cannot be defined as class methods in the actual class.  This is consistent with
the lookup of special methods that are called on instances, only in this
case the instance is itself a class.

.. seealso::

   :pep:`3119` - Introducing Abstract Base Classes
      Includes the specification for customizing :func:`isinstance` and
      :func:`issubclass` behavior through :meth:`~class.__instancecheck__` and
      :meth:`~class.__subclasscheck__`, with motivation for this functionality
      in the context of adding Abstract Base Classes (see the :mod:`abc`
      module) to the language.


.. _callable-types:

Emulating callable objects
--------------------------


.. method:: object.__call__(self[, args...])

   .. index:: pair: call; instance

   Called when the instance is "called" as a function; if this method is defined,
   ``x(arg1, arg2, ...)`` is a shorthand for ``x.__call__(arg1, arg2, ...)``.


.. _sequence-types:

Emulating container types
-------------------------

The following methods can be defined to implement container objects.  Containers
usually are sequences (such as lists or tuples) or mappings (like dictionaries),
but can represent other containers as well.  The first set of methods is used
either to emulate a sequence or to emulate a mapping; the difference is that for
a sequence, the allowable keys should be the integers *k* for which ``0 <= k <
N`` where *N* is the length of the sequence, or slice objects, which define a
range of items. (For backwards compatibility, the method :meth:`__getslice__`
(see below) can also be defined to handle simple, but not extended slices.) It
is also recommended that mappings provide the methods :meth:`keys`,
:meth:`values`, :meth:`items`, :meth:`has_key`, :meth:`get`, :meth:`clear`,
:meth:`setdefault`, :meth:`iterkeys`, :meth:`itervalues`, :meth:`iteritems`,
:meth:`pop`, :meth:`popitem`, :meth:`!copy`, and :meth:`update` behaving similar
to those for Python's standard dictionary objects.  The :mod:`UserDict` module
provides a :class:`DictMixin` class to help create those methods from a base set
of :meth:`__getitem__`, :meth:`__setitem__`, :meth:`__delitem__`, and
:meth:`keys`. Mutable sequences should provide methods :meth:`append`,
:meth:`count`, :meth:`index`, :meth:`extend`, :meth:`insert`, :meth:`pop`,
:meth:`remove`, :meth:`reverse` and :meth:`sort`, like Python standard list
objects.  Finally, sequence types should implement addition (meaning
concatenation) and multiplication (meaning repetition) by defining the methods
:meth:`__add__`, :meth:`__radd__`, :meth:`__iadd__`, :meth:`__mul__`,
:meth:`__rmul__` and :meth:`__imul__` described below; they should not define
:meth:`__coerce__` or other numerical operators.  It is recommended that both
mappings and sequences implement the :meth:`__contains__` method to allow
efficient use of the ``in`` operator; for mappings, ``in`` should be equivalent
of :meth:`has_key`; for sequences, it should search through the values.  It is
further recommended that both mappings and sequences implement the
:meth:`__iter__` method to allow efficient iteration through the container; for
mappings, :meth:`__iter__` should be the same as :meth:`iterkeys`; for
sequences, it should iterate through the values.


.. method:: object.__len__(self)

   .. index::
      builtin: len
      single: __nonzero__() (object method)

   Called to implement the built-in function :func:`len`.  Should return the length
   of the object, an integer ``>=`` 0.  Also, an object that doesn't define a
   :meth:`__nonzero__` method and whose :meth:`__len__` method returns zero is
   considered to be false in a Boolean context.

   .. impl-detail::

      In CPython, the length is required to be at most :attr:`sys.maxsize`.
      If the length is larger than :attr:`!sys.maxsize` some features (such as
      :func:`len`) may raise :exc:`OverflowError`.  To prevent raising
      :exc:`!OverflowError` by truth value testing, an object must define a
      :meth:`__nonzero__` method.


.. method:: object.__getitem__(self, key)

   .. index:: object: slice

   Called to implement evaluation of ``self[key]``. For sequence types, the
   accepted keys should be integers and slice objects.  Note that the special
   interpretation of negative indexes (if the class wishes to emulate a sequence
   type) is up to the :meth:`__getitem__` method. If *key* is of an inappropriate
   type, :exc:`TypeError` may be raised; if of a value outside the set of indexes
   for the sequence (after any special interpretation of negative values),
   :exc:`IndexError` should be raised. For mapping types, if *key* is missing (not
   in the container), :exc:`KeyError` should be raised.

   .. note::

      :keyword:`for` loops expect that an :exc:`IndexError` will be raised for illegal
      indexes to allow proper detection of the end of the sequence.


.. method:: object.__missing__(self, key)

   Called by :class:`dict`\ .\ :meth:`__getitem__` to implement ``self[key]`` for dict subclasses
   when key is not in the dictionary.


.. method:: object.__setitem__(self, key, value)

   Called to implement assignment to ``self[key]``.  Same note as for
   :meth:`__getitem__`.  This should only be implemented for mappings if the
   objects support changes to the values for keys, or if new keys can be added, or
   for sequences if elements can be replaced.  The same exceptions should be raised
   for improper *key* values as for the :meth:`__getitem__` method.


.. method:: object.__delitem__(self, key)

   Called to implement deletion of ``self[key]``.  Same note as for
   :meth:`__getitem__`.  This should only be implemented for mappings if the
   objects support removal of keys, or for sequences if elements can be removed
   from the sequence.  The same exceptions should be raised for improper *key*
   values as for the :meth:`__getitem__` method.


.. method:: object.__iter__(self)

   This method is called when an iterator is required for a container. This method
   should return a new iterator object that can iterate over all the objects in the
   container.  For mappings, it should iterate over the keys of the container, and
   should also be made available as the method :meth:`iterkeys`.

   Iterator objects also need to implement this method; they are required to return
   themselves.  For more information on iterator objects, see :ref:`typeiter`.


.. method:: object.__reversed__(self)

   Called (if present) by the :func:`reversed` built-in to implement
   reverse iteration.  It should return a new iterator object that iterates
   over all the objects in the container in reverse order.

   If the :meth:`__reversed__` method is not provided, the :func:`reversed`
   built-in will fall back to using the sequence protocol (:meth:`__len__` and
   :meth:`__getitem__`).  Objects that support the sequence protocol should
   only provide :meth:`__reversed__` if they can provide an implementation
   that is more efficient than the one provided by :func:`reversed`.

   .. versionadded:: 2.6


The membership test operators (:keyword:`in` and :keyword:`not in`) are normally
implemented as an iteration through a sequence.  However, container objects can
supply the following special method with a more efficient implementation, which
also does not require the object be a sequence.

.. method:: object.__contains__(self, item)

   Called to implement membership test operators.  Should return true if *item*
   is in *self*, false otherwise.  For mapping objects, this should consider the
   keys of the mapping rather than the values or the key-item pairs.

   For objects that don't define :meth:`__contains__`, the membership test first
   tries iteration via :meth:`__iter__`, then the old sequence iteration
   protocol via :meth:`__getitem__`, see :ref:`this section in the language
   reference <membership-test-details>`.


.. _sequence-methods:

Additional methods for emulation of sequence types
--------------------------------------------------

The following optional methods can be defined to further emulate sequence
objects.  Immutable sequences methods should at most only define
:meth:`__getslice__`; mutable sequences might define all three methods.


.. method:: object.__getslice__(self, i, j)

   .. deprecated:: 2.0
      Support slice objects as parameters to the :meth:`__getitem__` method.
      (However, built-in types in CPython currently still implement
      :meth:`__getslice__`.  Therefore, you have to override it in derived
      classes when implementing slicing.)

   Called to implement evaluation of ``self[i:j]``. The returned object should
   be of the same type as *self*.  Note that missing *i* or *j* in the slice
   expression are replaced by zero or :attr:`sys.maxsize`, respectively.  If
   negative indexes are used in the slice, the length of the sequence is added
   to that index. If the instance does not implement the :meth:`__len__` method,
   an :exc:`AttributeError` is raised. No guarantee is made that indexes
   adjusted this way are not still negative.  Indexes which are greater than the
   length of the sequence are not modified. If no :meth:`__getslice__` is found,
   a slice object is created instead, and passed to :meth:`__getitem__` instead.


.. method:: object.__setslice__(self, i, j, sequence)

   Called to implement assignment to ``self[i:j]``. Same notes for *i* and *j* as
   for :meth:`__getslice__`.

   This method is deprecated. If no :meth:`__setslice__` is found, or for extended
   slicing of the form ``self[i:j:k]``, a slice object is created, and passed to
   :meth:`__setitem__`, instead of :meth:`__setslice__` being called.


.. method:: object.__delslice__(self, i, j)

   Called to implement deletion of ``self[i:j]``. Same notes for *i* and *j* as for
   :meth:`__getslice__`. This method is deprecated. If no :meth:`__delslice__` is
   found, or for extended slicing of the form ``self[i:j:k]``, a slice object is
   created, and passed to :meth:`__delitem__`, instead of :meth:`__delslice__`
   being called.

Notice that these methods are only invoked when a single slice with a single
colon is used, and the slice method is available.  For slice operations
involving extended slice notation, or in absence of the slice methods,
:meth:`__getitem__`, :meth:`__setitem__` or :meth:`__delitem__` is called with a
slice object as argument.

The following example demonstrate how to make your program or module compatible
with earlier versions of Python (assuming that methods :meth:`__getitem__`,
:meth:`__setitem__` and :meth:`__delitem__` support slice objects as
arguments)::

   class MyClass:
       ...
       def __getitem__(self, index):
           ...
       def __setitem__(self, index, value):
           ...
       def __delitem__(self, index):
           ...

       if sys.version_info < (2, 0):
           # They won't be defined if version is at least 2.0 final

           def __getslice__(self, i, j):
               return self[max(0, i):max(0, j):]
           def __setslice__(self, i, j, seq):
               self[max(0, i):max(0, j):] = seq
           def __delslice__(self, i, j):
               del self[max(0, i):max(0, j):]
       ...

Note the calls to :func:`max`; these are necessary because of the handling of
negative indices before the :meth:`__\*slice__` methods are called.  When
negative indexes are used, the :meth:`__\*item__` methods receive them as
provided, but the :meth:`__\*slice__` methods get a "cooked" form of the index
values.  For each negative index value, the length of the sequence is added to
the index before calling the method (which may still result in a negative
index); this is the customary handling of negative indexes by the built-in
sequence types, and the :meth:`__\*item__` methods are expected to do this as
well.  However, since they should already be doing that, negative indexes cannot
be passed in; they must be constrained to the bounds of the sequence before
being passed to the :meth:`__\*item__` methods. Calling ``max(0, i)``
conveniently returns the proper value.


.. _numeric-types:

Emulating numeric types
-----------------------

The following methods can be defined to emulate numeric objects. Methods
corresponding to operations that are not supported by the particular kind of
number implemented (e.g., bitwise operations for non-integral numbers) should be
left undefined.


.. method:: object.__add__(self, other)
            object.__sub__(self, other)
            object.__mul__(self, other)
            object.__floordiv__(self, other)
            object.__mod__(self, other)
            object.__divmod__(self, other)
            object.__pow__(self, other[, modulo])
            object.__lshift__(self, other)
            object.__rshift__(self, other)
            object.__and__(self, other)
            object.__xor__(self, other)
            object.__or__(self, other)

   .. index::
      builtin: divmod
      builtin: pow
      builtin: pow

   These methods are called to implement the binary arithmetic operations (``+``,
   ``-``, ``*``, ``//``, ``%``, :func:`divmod`, :func:`pow`, ``**``, ``<<``,
   ``>>``, ``&``, ``^``, ``|``).  For instance, to evaluate the expression
   ``x + y``, where *x* is an instance of a class that has an :meth:`__add__`
   method, ``x.__add__(y)`` is called.  The :meth:`__divmod__` method should be the
   equivalent to using :meth:`__floordiv__` and :meth:`__mod__`; it should not be
   related to :meth:`__truediv__` (described below).  Note that :meth:`__pow__`
   should be defined to accept an optional third argument if the ternary version of
   the built-in :func:`pow` function is to be supported.

   If one of those methods does not support the operation with the supplied
   arguments, it should return ``NotImplemented``.


.. method:: object.__div__(self, other)
            object.__truediv__(self, other)

   The division operator (``/``) is implemented by these methods.  The
   :meth:`__truediv__` method is used when ``__future__.division`` is in effect,
   otherwise :meth:`__div__` is used.  If only one of these two methods is defined,
   the object will not support division in the alternate context; :exc:`TypeError`
   will be raised instead.


.. method:: object.__radd__(self, other)
            object.__rsub__(self, other)
            object.__rmul__(self, other)
            object.__rdiv__(self, other)
            object.__rtruediv__(self, other)
            object.__rfloordiv__(self, other)
            object.__rmod__(self, other)
            object.__rdivmod__(self, other)
            object.__rpow__(self, other)
            object.__rlshift__(self, other)
            object.__rrshift__(self, other)
            object.__rand__(self, other)
            object.__rxor__(self, other)
            object.__ror__(self, other)

   .. index::
      builtin: divmod
      builtin: pow

   These methods are called to implement the binary arithmetic operations (``+``,
   ``-``, ``*``, ``/``, ``%``, :func:`divmod`, :func:`pow`, ``**``, ``<<``, ``>>``,
   ``&``, ``^``, ``|``) with reflected (swapped) operands.  These functions are
   only called if the left operand does not support the corresponding operation and
   the operands are of different types. [#]_ For instance, to evaluate the
   expression ``x - y``, where *y* is an instance of a class that has an
   :meth:`__rsub__` method, ``y.__rsub__(x)`` is called if ``x.__sub__(y)`` returns
   *NotImplemented*.

   .. index:: builtin: pow

   Note that ternary :func:`pow` will not try calling :meth:`__rpow__` (the
   coercion rules would become too complicated).

   .. note::

      If the right operand's type is a subclass of the left operand's type and that
      subclass provides the reflected method for the operation, this method will be
      called before the left operand's non-reflected method.  This behavior allows
      subclasses to override their ancestors' operations.


.. method:: object.__iadd__(self, other)
            object.__isub__(self, other)
            object.__imul__(self, other)
            object.__idiv__(self, other)
            object.__itruediv__(self, other)
            object.__ifloordiv__(self, other)
            object.__imod__(self, other)
            object.__ipow__(self, other[, modulo])
            object.__ilshift__(self, other)
            object.__irshift__(self, other)
            object.__iand__(self, other)
            object.__ixor__(self, other)
            object.__ior__(self, other)

   These methods are called to implement the augmented arithmetic assignments
   (``+=``, ``-=``, ``*=``, ``/=``, ``//=``, ``%=``, ``**=``, ``<<=``, ``>>=``,
   ``&=``, ``^=``, ``|=``).  These methods should attempt to do the operation
   in-place (modifying *self*) and return the result (which could be, but does
   not have to be, *self*).  If a specific method is not defined, the augmented
   assignment falls back to the normal methods.  For instance, to execute the
   statement ``x += y``, where *x* is an instance of a class that has an
   :meth:`__iadd__` method, ``x.__iadd__(y)`` is called.  If *x* is an instance
   of a class that does not define a :meth:`__iadd__` method, ``x.__add__(y)``
   and ``y.__radd__(x)`` are considered, as with the evaluation of ``x + y``.


.. method:: object.__neg__(self)
            object.__pos__(self)
            object.__abs__(self)
            object.__invert__(self)

   .. index:: builtin: abs

   Called to implement the unary arithmetic operations (``-``, ``+``, :func:`abs`
   and ``~``).


.. method:: object.__complex__(self)
            object.__int__(self)
            object.__long__(self)
            object.__float__(self)

   .. index::
      builtin: complex
      builtin: int
      builtin: long
      builtin: float

   Called to implement the built-in functions :func:`complex`, :func:`int`,
   :func:`long`, and :func:`float`.  Should return a value of the appropriate type.


.. method:: object.__oct__(self)
            object.__hex__(self)

   .. index::
      builtin: oct
      builtin: hex

   Called to implement the built-in functions :func:`oct` and :func:`hex`.  Should
   return a string value.


.. method:: object.__index__(self)

   Called to implement :func:`operator.index`.  Also called whenever Python needs
   an integer object (such as in slicing).  Must return an integer (int or long).

   .. versionadded:: 2.5


.. method:: object.__coerce__(self, other)

   Called to implement "mixed-mode" numeric arithmetic.  Should either return a
   2-tuple containing *self* and *other* converted to a common numeric type, or
   ``None`` if conversion is impossible.  When the common type would be the type of
   ``other``, it is sufficient to return ``None``, since the interpreter will also
   ask the other object to attempt a coercion (but sometimes, if the implementation
   of the other type cannot be changed, it is useful to do the conversion to the
   other type here).  A return value of ``NotImplemented`` is equivalent to
   returning ``None``.


.. _coercion-rules:

Coercion rules
--------------

This section used to document the rules for coercion.  As the language has
evolved, the coercion rules have become hard to document precisely; documenting
what one version of one particular implementation does is undesirable.  Instead,
here are some informal guidelines regarding coercion.  In Python 3, coercion
will not be supported.

*

  If the left operand of a % operator is a string or Unicode object, no coercion
  takes place and the string formatting operation is invoked instead.

*

  It is no longer recommended to define a coercion operation. Mixed-mode
  operations on types that don't define coercion pass the original arguments to
  the operation.

*

  New-style classes (those derived from :class:`object`) never invoke the
  :meth:`__coerce__` method in response to a binary operator; the only time
  :meth:`__coerce__` is invoked is when the built-in function :func:`coerce` is
  called.

*

  For most intents and purposes, an operator that returns ``NotImplemented`` is
  treated the same as one that is not implemented at all.

*

  Below, :meth:`__op__` and :meth:`__rop__` are used to signify the generic method
  names corresponding to an operator; :meth:`__iop__` is used for the
  corresponding in-place operator.  For example, for the operator '``+``',
  :meth:`__add__` and :meth:`__radd__` are used for the left and right variant of
  the binary operator, and :meth:`__iadd__` for the in-place variant.

*

  For objects *x* and *y*, first ``x.__op__(y)`` is tried.  If this is not
  implemented or returns ``NotImplemented``, ``y.__rop__(x)`` is tried.  If this
  is also not implemented or returns ``NotImplemented``, a :exc:`TypeError`
  exception is raised.  But see the following exception:

*

  Exception to the previous item: if the left operand is an instance of a built-in
  type or a new-style class, and the right operand is an instance of a proper
  subclass of that type or class and overrides the base's :meth:`__rop__` method,
  the right operand's :meth:`__rop__` method is tried *before* the left operand's
  :meth:`__op__` method.

  This is done so that a subclass can completely override binary operators.
  Otherwise, the left operand's :meth:`__op__` method would always accept the
  right operand: when an instance of a given class is expected, an instance of a
  subclass of that class is always acceptable.

*

  When either operand type defines a coercion, this coercion is called before that
  type's :meth:`__op__` or :meth:`__rop__` method is called, but no sooner.  If
  the coercion returns an object of a different type for the operand whose
  coercion is invoked, part of the process is redone using the new object.

*

  When an in-place operator (like '``+=``') is used, if the left operand
  implements :meth:`__iop__`, it is invoked without any coercion.  When the
  operation falls back to :meth:`__op__` and/or :meth:`__rop__`, the normal
  coercion rules apply.

*

  In ``x + y``, if *x* is a sequence that implements sequence concatenation,
  sequence concatenation is invoked.

*

  In ``x * y``, if one operand is a sequence that implements sequence
  repetition, and the other is an integer (:class:`int` or :class:`long`),
  sequence repetition is invoked.

*

  Rich comparisons (implemented by methods :meth:`__eq__` and so on) never use
  coercion.  Three-way comparison (implemented by :meth:`__cmp__`) does use
  coercion under the same conditions as other binary operations use it.

*

  In the current implementation, the built-in numeric types :class:`int`,
  :class:`long`, :class:`float`, and :class:`complex` do not use coercion.
  All these types implement a :meth:`__coerce__` method, for use by the built-in
  :func:`coerce` function.

  .. versionchanged:: 2.7

     The complex type no longer makes implicit calls to the :meth:`__coerce__`
     method for mixed-type binary arithmetic operations.


.. _context-managers:

With Statement Context Managers
-------------------------------

.. versionadded:: 2.5

A :dfn:`context manager` is an object that defines the runtime context to be
established when executing a :keyword:`with` statement. The context manager
handles the entry into, and the exit from, the desired runtime context for the
execution of the block of code.  Context managers are normally invoked using the
:keyword:`with` statement (described in section :ref:`with`), but can also be
used by directly invoking their methods.

.. index::
   statement: with
   single: context manager

Typical uses of context managers include saving and restoring various kinds of
global state, locking and unlocking resources, closing opened files, etc.

For more information on context managers, see :ref:`typecontextmanager`.


.. method:: object.__enter__(self)

   Enter the runtime context related to this object. The :keyword:`with` statement
   will bind this method's return value to the target(s) specified in the
   :keyword:`as` clause of the statement, if any.


.. method:: object.__exit__(self, exc_type, exc_value, traceback)

   Exit the runtime context related to this object. The parameters describe the
   exception that caused the context to be exited. If the context was exited
   without an exception, all three arguments will be :const:`None`.

   If an exception is supplied, and the method wishes to suppress the exception
   (i.e., prevent it from being propagated), it should return a true value.
   Otherwise, the exception will be processed normally upon exit from this method.

   Note that :meth:`__exit__` methods should not reraise the passed-in exception;
   this is the caller's responsibility.


.. seealso::

   :pep:`343` - The "with" statement
      The specification, background, and examples for the Python :keyword:`with`
      statement.


.. _old-style-special-lookup:

Special method lookup for old-style classes
-------------------------------------------

For old-style classes, special methods are always looked up in exactly the
same way as any other method or attribute. This is the case regardless of
whether the method is being looked up explicitly as in ``x.__getitem__(i)``
or implicitly as in ``x[i]``.

This behaviour means that special methods may exhibit different behaviour
for different instances of a single old-style class if the appropriate
special attributes are set differently::

   >>> class C:
   ...     pass
   ...
   >>> c1 = C()
   >>> c2 = C()
   >>> c1.__len__ = lambda: 5
   >>> c2.__len__ = lambda: 9
   >>> len(c1)
   5
   >>> len(c2)
   9


.. _new-style-special-lookup:

Special method lookup for new-style classes
-------------------------------------------

For new-style classes, implicit invocations of special methods are only guaranteed
to work correctly if defined on an object's type, not in the object's instance
dictionary.  That behaviour is the reason why the following code raises an
exception (unlike the equivalent example with old-style classes)::

   >>> class C(object):
   ...     pass
   ...
   >>> c = C()
   >>> c.__len__ = lambda: 5
   >>> len(c)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: object of type 'C' has no len()

The rationale behind this behaviour lies with a number of special methods such
as :meth:`__hash__` and :meth:`__repr__` that are implemented by all objects,
including type objects. If the implicit lookup of these methods used the
conventional lookup process, they would fail when invoked on the type object
itself::

   >>> 1 .__hash__() == hash(1)
   True
   >>> int.__hash__() == hash(int)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: descriptor '__hash__' of 'int' object needs an argument

Incorrectly attempting to invoke an unbound method of a class in this way is
sometimes referred to as 'metaclass confusion', and is avoided by bypassing
the instance when looking up special methods::

   >>> type(1).__hash__(1) == hash(1)
   True
   >>> type(int).__hash__(int) == hash(int)
   True

In addition to bypassing any instance attributes in the interest of
correctness, implicit special method lookup generally also bypasses the
:meth:`__getattribute__` method even of the object's metaclass::

   >>> class Meta(type):
   ...    def __getattribute__(*args):
   ...       print "Metaclass getattribute invoked"
   ...       return type.__getattribute__(*args)
   ...
   >>> class C(object):
   ...     __metaclass__ = Meta
   ...     def __len__(self):
   ...         return 10
   ...     def __getattribute__(*args):
   ...         print "Class getattribute invoked"
   ...         return object.__getattribute__(*args)
   ...
   >>> c = C()
   >>> c.__len__()                 # Explicit lookup via instance
   Class getattribute invoked
   10
   >>> type(c).__len__(c)          # Explicit lookup via type
   Metaclass getattribute invoked
   10
   >>> len(c)                      # Implicit lookup
   10

Bypassing the :meth:`__getattribute__` machinery in this fashion
provides significant scope for speed optimisations within the
interpreter, at the cost of some flexibility in the handling of
special methods (the special method *must* be set on the class
object itself in order to be consistently invoked by the interpreter).


.. rubric:: Footnotes

.. [#] It *is* possible in some cases to change an object's type, under certain
   controlled conditions. It generally isn't a good idea though, since it can
   lead to some very strange behaviour if it is handled incorrectly.

.. [#] For operands of the same type, it is assumed that if the non-reflected method
   (such as :meth:`__add__`) fails the operation is not supported, which is why the
   reflected method is not called.

