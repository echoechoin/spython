:mod:`json` --- JSON encoder and decoder
========================================

.. module:: json
   :synopsis: Encode and decode the JSON format.
.. moduleauthor:: Bob Ippolito <bob@redivi.com>
.. sectionauthor:: Bob Ippolito <bob@redivi.com>
.. versionadded:: 2.6

`JSON (JavaScript Object Notation) <http://json.org>`_, specified by
:rfc:`7159` (which obsoletes :rfc:`4627`) and by
`ECMA-404 <http://www.ecma-international.org/publications/standards/Ecma-404.htm>`_,
is a lightweight data interchange format inspired by
`JavaScript <https://en.wikipedia.org/wiki/JavaScript>`_ object literal syntax
(although it is not a strict subset of JavaScript [#rfc-errata]_ ).

:mod:`json` exposes an API familiar to users of the standard library
:mod:`marshal` and :mod:`pickle` modules.

Encoding basic Python object hierarchies::

    >>> import json
    >>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    >>> print json.dumps("\"foo\bar")
    "\"foo\bar"
    >>> print json.dumps(u'\u1234')
    "\u1234"
    >>> print json.dumps('\\')
    "\\"
    >>> print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
    {"a": 0, "b": 0, "c": 0}
    >>> from StringIO import StringIO
    >>> io = StringIO()
    >>> json.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]'

Compact encoding::

    >>> import json
    >>> json.dumps([1,2,3,{'4': 5, '6': 7}], separators=(',',':'))
    '[1,2,3,{"4":5,"6":7}]'

Pretty printing::

    >>> import json
    >>> print json.dumps({'4': 5, '6': 7}, sort_keys=True,
    ...                  indent=4, separators=(',', ': '))
    {
        "4": 5,
        "6": 7
    }

Decoding JSON::

    >>> import json
    >>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    [u'foo', {u'bar': [u'baz', None, 1.0, 2]}]
    >>> json.loads('"\\"foo\\bar"')
    u'"foo\x08ar'
    >>> from StringIO import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)
    [u'streaming API']

Specializing JSON object decoding::

    >>> import json
    >>> def as_complex(dct):
    ...     if '__complex__' in dct:
    ...         return complex(dct['real'], dct['imag'])
    ...     return dct
    ...
    >>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
    ...     object_hook=as_complex)
    (1+2j)
    >>> import decimal
    >>> json.loads('1.1', parse_float=decimal.Decimal)
    Decimal('1.1')

Extending :class:`JSONEncoder`::

    >>> import json
    >>> class ComplexEncoder(json.JSONEncoder):
    ...     def default(self, obj):
    ...         if isinstance(obj, complex):
    ...             return [obj.real, obj.imag]
    ...         # Let the base class default method raise the TypeError
    ...         return json.JSONEncoder.default(self, obj)
    ...
    >>> json.dumps(2 + 1j, cls=ComplexEncoder)
    '[2.0, 1.0]'
    >>> ComplexEncoder().encode(2 + 1j)
    '[2.0, 1.0]'
    >>> list(ComplexEncoder().iterencode(2 + 1j))
    ['[', '2.0', ', ', '1.0', ']']


.. highlight:: none

Using :mod:`json.tool` from the shell to validate and pretty-print::

    $ echo '{"json":"obj"}' | python -m json.tool
    {
        "json": "obj"
    }
    $ echo '{1.2:3.4}' | python -mjson.tool
    Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

.. highlight:: python

.. note::

   JSON is a subset of `YAML <http://yaml.org/>`_ 1.2.  The JSON produced by
   this module's default settings (in particular, the default *separators*
   value) is also a subset of YAML 1.0 and 1.1.  This module can thus also be
   used as a YAML serializer.


Basic Usage
-----------

.. function:: dump(obj, fp, skipkeys=False, ensure_ascii=True, \
                   check_circular=True, allow_nan=True, cls=None, \
                   indent=None, separators=None, encoding="utf-8", \
                   default=None, sort_keys=False, **kw)

   Serialize *obj* as a JSON formatted stream to *fp* (a ``.write()``-supporting
   :term:`file-like object`) using this :ref:`conversion table
   <py-to-json-table>`.

   If *skipkeys* is true (default: ``False``), then dict keys that are not
   of a basic type (:class:`str`, :class:`unicode`, :class:`int`, :class:`long`,
   :class:`float`, :class:`bool`, ``None``) will be skipped instead of raising a
   :exc:`TypeError`.

   If *ensure_ascii* is true (the default), all non-ASCII characters in the
   output are escaped with ``\uXXXX`` sequences, and the result is a
   :class:`str` instance consisting of ASCII characters only.  If
   *ensure_ascii* is false, some chunks written to *fp* may be
   :class:`unicode` instances.  This usually happens because the input contains
   unicode strings or the *encoding* parameter is used.  Unless ``fp.write()``
   explicitly understands :class:`unicode` (as in :func:`codecs.getwriter`)
   this is likely to cause an error.

   If *check_circular* is false (default: ``True``), then the circular
   reference check for container types will be skipped and a circular reference
   will result in an :exc:`OverflowError` (or worse).

   If *allow_nan* is false (default: ``True``), then it will be a
   :exc:`ValueError` to serialize out of range :class:`float` values (``nan``,
   ``inf``, ``-inf``) in strict compliance of the JSON specification.
   If *allow_nan* is true, their JavaScript equivalents (``NaN``,
   ``Infinity``, ``-Infinity``) will be used.

   If *indent* is a non-negative integer, then JSON array elements and object
   members will be pretty-printed with that indent level.  An indent level of 0,
   or negative, will only insert newlines.  ``None`` (the default) selects the
   most compact representation.

   .. note::

      Since the default item separator is ``', '``,  the output might include
      trailing whitespace when *indent* is specified.  You can use
      ``separators=(',', ': ')`` to avoid this.

   If specified, *separators* should be an ``(item_separator, key_separator)``
   tuple.  By default, ``(', ', ': ')`` are used.  To get the most compact JSON
   representation, you should specify ``(',', ':')`` to eliminate whitespace.

   *encoding* is the character encoding for str instances, default is UTF-8.

   If specified, *default* should be a function that gets called for objects that
   can't otherwise be serialized.  It should return a JSON encodable version of
   the object or raise a :exc:`TypeError`.  If not specified, :exc:`TypeError`
   is raised.

   If *sort_keys* is true (default: ``False``), then the output of
   dictionaries will be sorted by key.

   To use a custom :class:`JSONEncoder` subclass (e.g. one that overrides the
   :meth:`default` method to serialize additional types), specify it with the
   *cls* kwarg; otherwise :class:`JSONEncoder` is used.

   .. note::

      Unlike :mod:`pickle` and :mod:`marshal`, JSON is not a framed protocol so
      trying to serialize more objects with repeated calls to :func:`dump` and
      the same *fp* will result in an invalid JSON file.

.. function:: dumps(obj, skipkeys=False, ensure_ascii=True, \
                    check_circular=True, allow_nan=True, cls=None, \
                    indent=None, separators=None, encoding="utf-8", \
                    default=None, sort_keys=False, **kw)

   Serialize *obj* to a JSON formatted :class:`str` using this :ref:`conversion
   table <py-to-json-table>`.  If *ensure_ascii* is false, the result may
   contain non-ASCII characters and the return value may be a :class:`unicode`
   instance.

   The arguments have the same meaning as in :func:`dump`.

   .. note::

      Keys in key/value pairs of JSON are always of the type :class:`str`. When
      a dictionary is converted into JSON, all the keys of the dictionary are
      coerced to strings. As a result of this, if a dictionary is converted
      into JSON and then back into a dictionary, the dictionary may not equal
      the original one. That is, ``loads(dumps(x)) != x`` if x has non-string
      keys.

.. function:: load(fp[, encoding[, cls[, object_hook[, parse_float[, parse_int[, parse_constant[, object_pairs_hook[, **kw]]]]]]]])

   Deserialize *fp* (a ``.read()``-supporting :term:`file-like object`
   containing a JSON document) to a Python object using this :ref:`conversion
   table <json-to-py-table>`.

   If the contents of *fp* are encoded with an ASCII based encoding other than
   UTF-8 (e.g. latin-1), then an appropriate *encoding* name must be specified.
   Encodings that are not ASCII based (such as UCS-2) are not allowed, and
   should be wrapped with ``codecs.getreader(encoding)(fp)``, or simply decoded
   to a :class:`unicode` object and passed to :func:`loads`.

   *object_hook* is an optional function that will be called with the result of
   any object literal decoded (a :class:`dict`).  The return value of
   *object_hook* will be used instead of the :class:`dict`.  This feature can be used
   to implement custom decoders (e.g. `JSON-RPC <http://www.jsonrpc.org>`_
   class hinting).

   *object_pairs_hook* is an optional function that will be called with the
   result of any object literal decoded with an ordered list of pairs.  The
   return value of *object_pairs_hook* will be used instead of the
   :class:`dict`.  This feature can be used to implement custom decoders that
   rely on the order that the key and value pairs are decoded (for example,
   :func:`collections.OrderedDict` will remember the order of insertion). If
   *object_hook* is also defined, the *object_pairs_hook* takes priority.

   .. versionchanged:: 2.7
      Added support for *object_pairs_hook*.

   *parse_float*, if specified, will be called with the string of every JSON
   float to be decoded.  By default, this is equivalent to ``float(num_str)``.
   This can be used to use another datatype or parser for JSON floats
   (e.g. :class:`decimal.Decimal`).

   *parse_int*, if specified, will be called with the string of every JSON int
   to be decoded.  By default, this is equivalent to ``int(num_str)``.  This can
   be used to use another datatype or parser for JSON integers
   (e.g. :class:`float`).

   *parse_constant*, if specified, will be called with one of the following
   strings: ``'-Infinity'``, ``'Infinity'``, ``'NaN'``.
   This can be used to raise an exception if invalid JSON numbers
   are encountered.

   .. versionchanged:: 2.7
      *parse_constant* doesn't get called on 'null', 'true', 'false' anymore.

   To use a custom :class:`JSONDecoder` subclass, specify it with the ``cls``
   kwarg; otherwise :class:`JSONDecoder` is used.  Additional keyword arguments
   will be passed to the constructor of the class.


.. function:: loads(s[, encoding[, cls[, object_hook[, parse_float[, parse_int[, parse_constant[, object_pairs_hook[, **kw]]]]]]]])

   Deserialize *s* (a :class:`str` or :class:`unicode` instance containing a JSON
   document) to a Python object using this :ref:`conversion table
   <json-to-py-table>`.

   If *s* is a :class:`str` instance and is encoded with an ASCII based encoding
   other than UTF-8 (e.g. latin-1), then an appropriate *encoding* name must be
   specified.  Encodings that are not ASCII based (such as UCS-2) are not
   allowed and should be decoded to :class:`unicode` first.

   The other arguments have the same meaning as in :func:`load`.


Encoders and Decoders
---------------------

.. class:: JSONDecoder([encoding[, object_hook[, parse_float[, parse_int[, parse_constant[, strict[, object_pairs_hook]]]]]]])

   Simple JSON decoder.

   Performs the following translations in decoding by default:

   .. _json-to-py-table:

   +---------------+-------------------+
   | JSON          | Python            |
   +===============+===================+
   | object        | dict              |
   +---------------+-------------------+
   | array         | list              |
   +---------------+-------------------+
   | string        | unicode           |
   +---------------+-------------------+
   | number (int)  | int, long         |
   +---------------+-------------------+
   | number (real) | float             |
   +---------------+-------------------+
   | true          | True              |
   +---------------+-------------------+
   | false         | False             |
   +---------------+-------------------+
   | null          | None              |
   +---------------+-------------------+

   It also understands ``NaN``, ``Infinity``, and ``-Infinity`` as their
   corresponding ``float`` values, which is outside the JSON spec.

   *encoding* determines the encoding used to interpret any :class:`str` objects
   decoded by this instance (UTF-8 by default).  It has no effect when decoding
   :class:`unicode` objects.

   Note that currently only encodings that are a superset of ASCII work, strings
   of other encodings should be passed in as :class:`unicode`.

   *object_hook*, if specified, will be called with the result of every JSON
   object decoded and its return value will be used in place of the given
   :class:`dict`.  This can be used to provide custom deserializations (e.g. to
   support JSON-RPC class hinting).

   *object_pairs_hook*, if specified will be called with the result of every
   JSON object decoded with an ordered list of pairs.  The return value of
   *object_pairs_hook* will be used instead of the :class:`dict`.  This
   feature can be used to implement custom decoders that rely on the order
   that the key and value pairs are decoded (for example,
   :func:`collections.OrderedDict` will remember the order of insertion). If
   *object_hook* is also defined, the *object_pairs_hook* takes priority.

   .. versionchanged:: 2.7
      Added support for *object_pairs_hook*.

   *parse_float*, if specified, will be called with the string of every JSON
   float to be decoded.  By default, this is equivalent to ``float(num_str)``.
   This can be used to use another datatype or parser for JSON floats
   (e.g. :class:`decimal.Decimal`).

   *parse_int*, if specified, will be called with the string of every JSON int
   to be decoded.  By default, this is equivalent to ``int(num_str)``.  This can
   be used to use another datatype or parser for JSON integers
   (e.g. :class:`float`).

   *parse_constant*, if specified, will be called with one of the following
   strings: ``'-Infinity'``, ``'Infinity'``, ``'NaN'``.
   This can be used to raise an exception if invalid JSON numbers
   are encountered.

   If *strict* is false (``True`` is the default), then control characters
   will be allowed inside strings.  Control characters in this context are
   those with character codes in the 0--31 range, including ``'\t'`` (tab),
   ``'\n'``, ``'\r'`` and ``'\0'``.

   If the data being deserialized is not a valid JSON document, a
   :exc:`ValueError` will be raised.

   .. method:: decode(s)

      Return the Python representation of *s* (a :class:`str` or
      :class:`unicode` instance containing a JSON document).

   .. method:: raw_decode(s)

      Decode a JSON document from *s* (a :class:`str` or :class:`unicode`
      beginning with a JSON document) and return a 2-tuple of the Python
      representation and the index in *s* where the document ended.

      This can be used to decode a JSON document from a string that may have
      extraneous data at the end.


.. class:: JSONEncoder([skipkeys[, ensure_ascii[, check_circular[, allow_nan[, sort_keys[, indent[, separators[, encoding[, default]]]]]]]]])

   Extensible JSON encoder for Python data structures.

   Supports the following objects and types by default:

   .. _py-to-json-table:

   +-------------------+---------------+
   | Python            | JSON          |
   +===================+===============+
   | dict              | object        |
   +-------------------+---------------+
   | list, tuple       | array         |
   +-------------------+---------------+
   | str, unicode      | string        |
   +-------------------+---------------+
   | int, long, float  | number        |
   +-------------------+---------------+
   | True              | true          |
   +-------------------+---------------+
   | False             | false         |
   +-------------------+---------------+
   | None              | null          |
   +-------------------+---------------+

   To extend this to recognize other objects, subclass and implement a
   :meth:`default` method with another method that returns a serializable object
   for ``o`` if possible, otherwise it should call the superclass implementation
   (to raise :exc:`TypeError`).

   If *skipkeys* is false (the default), then it is a :exc:`TypeError` to
   attempt encoding of keys that are not str, int, long, float or ``None``.  If
   *skipkeys* is true, such items are simply skipped.

   If *ensure_ascii* is true (the default), all non-ASCII characters in the
   output are escaped with ``\uXXXX`` sequences, and the results are
   :class:`str` instances consisting of ASCII characters only. If
   *ensure_ascii* is false, a result may be a :class:`unicode`
   instance. This usually happens if the input contains unicode strings or the
   *encoding* parameter is used.

   If *check_circular* is true (the default), then lists, dicts, and custom
   encoded objects will be checked for circular references during encoding to
   prevent an infinite recursion (which would cause an :exc:`OverflowError`).
   Otherwise, no such check takes place.

   If *allow_nan* is true (the default), then ``NaN``, ``Infinity``, and
   ``-Infinity`` will be encoded as such.  This behavior is not JSON
   specification compliant, but is consistent with most JavaScript based
   encoders and decoders.  Otherwise, it will be a :exc:`ValueError` to encode
   such floats.

   If *sort_keys* is true (default: ``False``), then the output of dictionaries
   will be sorted by key; this is useful for regression tests to ensure that
   JSON serializations can be compared on a day-to-day basis.

   If *indent* is a non-negative integer (it is ``None`` by default), then JSON
   array elements and object members will be pretty-printed with that indent
   level.  An indent level of 0 will only insert newlines.  ``None`` is the most
   compact representation.

   .. note::

      Since the default item separator is ``', '``,  the output might include
      trailing whitespace when *indent* is specified.  You can use
      ``separators=(',', ': ')`` to avoid this.

   If specified, *separators* should be an ``(item_separator, key_separator)``
   tuple.  By default, ``(', ', ': ')`` are used.  To get the most compact JSON
   representation, you should specify ``(',', ':')`` to eliminate whitespace.

   If specified, *default* should be a function that gets called for objects that
   can't otherwise be serialized.  It should return a JSON encodable version of
   the object or raise a :exc:`TypeError`.  If not specified, :exc:`TypeError`
   is raised.

   If *encoding* is not ``None``, then all input strings will be transformed
   into unicode using that encoding prior to JSON-encoding.  The default is
   UTF-8.


   .. method:: default(o)

      Implement this method in a subclass such that it returns a serializable
      object for *o*, or calls the base implementation (to raise a
      :exc:`TypeError`).

      For example, to support arbitrary iterators, you could implement default
      like this::

         def default(self, o):
            try:
                iterable = iter(o)
            except TypeError:
                pass
            else:
                return list(iterable)
            # Let the base class default method raise the TypeError
            return JSONEncoder.default(self, o)


   .. method:: encode(o)

      Return a JSON string representation of a Python data structure, *o*.  For
      example::

        >>> JSONEncoder().encode({"foo": ["bar", "baz"]})
        '{"foo": ["bar", "baz"]}'


   .. method:: iterencode(o)

      Encode the given object, *o*, and yield each string representation as
      available.  For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)


Standard Compliance and Interoperability
----------------------------------------

The JSON format is specified by :rfc:`7159` and by
`ECMA-404 <http://www.ecma-international.org/publications/standards/Ecma-404.htm>`_.
This section details this module's level of compliance with the RFC.
For simplicity, :class:`JSONEncoder` and :class:`JSONDecoder` subclasses, and
parameters other than those explicitly mentioned, are not considered.

This module does not comply with the RFC in a strict fashion, implementing some
extensions that are valid JavaScript but not valid JSON.  In particular:

- Infinite and NaN number values are accepted and output;
- Repeated names within an object are accepted, and only the value of the last
  name-value pair is used.

Since the RFC permits RFC-compliant parsers to accept input texts that are not
RFC-compliant, this module's deserializer is technically RFC-compliant under
default settings.

Character Encodings
^^^^^^^^^^^^^^^^^^^

The RFC requires that JSON be represented using either UTF-8, UTF-16, or
UTF-32, with UTF-8 being the recommended default for maximum interoperability.
Accordingly, this module uses UTF-8 as the default for its *encoding* parameter.

This module's deserializer only directly works with ASCII-compatible encodings;
UTF-16, UTF-32, and other ASCII-incompatible encodings require the use of
workarounds described in the documentation for the deserializer's *encoding*
parameter.

As permitted, though not required, by the RFC, this module's serializer sets
*ensure_ascii=True* by default, thus escaping the output so that the resulting
strings only contain ASCII characters.

The RFC prohibits adding a byte order mark (BOM) to the start of a JSON text,
and this module's serializer does not add a BOM to its output.
The RFC permits, but does not require, JSON deserializers to ignore an initial
BOM in their input.  This module's deserializer raises a :exc:`ValueError`
when an initial BOM is present.

The RFC does not explicitly forbid JSON strings which contain byte sequences
that don't correspond to valid Unicode characters (e.g. unpaired UTF-16
surrogates), but it does note that they may cause interoperability problems.
By default, this module accepts and outputs (when present in the original
:class:`str`) code points for such sequences.


Infinite and NaN Number Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The RFC does not permit the representation of infinite or NaN number values.
Despite that, by default, this module accepts and outputs ``Infinity``,
``-Infinity``, and ``NaN`` as if they were valid JSON number literal values::

   >>> # Neither of these calls raises an exception, but the results are not valid JSON
   >>> json.dumps(float('-inf'))
   '-Infinity'
   >>> json.dumps(float('nan'))
   'NaN'
   >>> # Same when deserializing
   >>> json.loads('-Infinity')
   -inf
   >>> json.loads('NaN')
   nan

In the serializer, the *allow_nan* parameter can be used to alter this
behavior.  In the deserializer, the *parse_constant* parameter can be used to
alter this behavior.


Repeated Names Within an Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The RFC specifies that the names within a JSON object should be unique, but
does not mandate how repeated names in JSON objects should be handled.  By
default, this module does not raise an exception; instead, it ignores all but
the last name-value pair for a given name::

   >>> weird_json = '{"x": 1, "x": 2, "x": 3}'
   >>> json.loads(weird_json)
   {u'x': 3}

The *object_pairs_hook* parameter can be used to alter this behavior.


Top-level Non-Object, Non-Array Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The old version of JSON specified by the obsolete :rfc:`4627` required that
the top-level value of a JSON text must be either a JSON object or array
(Python :class:`dict` or :class:`list`), and could not be a JSON null,
boolean, number, or string value.  :rfc:`7159` removed that restriction, and
this module does not and has never implemented that restriction in either its
serializer or its deserializer.

Regardless, for maximum interoperability, you may wish to voluntarily adhere
to the restriction yourself.


Implementation Limitations
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some JSON deserializer implementations may set limits on:

* the size of accepted JSON texts
* the maximum level of nesting of JSON objects and arrays
* the range and precision of JSON numbers
* the content and maximum length of JSON strings

This module does not impose any such limits beyond those of the relevant
Python datatypes themselves or the Python interpreter itself.

When serializing to JSON, beware any such limitations in applications that may
consume your JSON.  In particular, it is common for JSON numbers to be
deserialized into IEEE 754 double precision numbers and thus subject to that
representation's range and precision limitations.  This is especially relevant
when serializing Python :class:`int` values of extremely large magnitude, or
when serializing instances of "exotic" numerical types such as
:class:`decimal.Decimal`.


.. rubric:: Footnotes

.. [#rfc-errata] As noted in `the errata for RFC 7159
   <https://www.rfc-editor.org/errata_search.php?rfc=7159>`_,
   JSON permits literal U+2028 (LINE SEPARATOR) and
   U+2029 (PARAGRAPH SEPARATOR) characters in strings, whereas JavaScript
   (as of ECMAScript Edition 5.1) does not.
