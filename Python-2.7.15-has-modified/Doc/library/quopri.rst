:mod:`quopri` --- Encode and decode MIME quoted-printable data
==============================================================

.. module:: quopri
   :synopsis: Encode and decode files using the MIME quoted-printable encoding.


.. index::
   pair: quoted-printable; encoding
   single: MIME; quoted-printable encoding

**Source code:** :source:`Lib/quopri.py`

--------------

This module performs quoted-printable transport encoding and decoding, as
defined in :rfc:`1521`: "MIME (Multipurpose Internet Mail Extensions) Part One:
Mechanisms for Specifying and Describing the Format of Internet Message Bodies".
The quoted-printable encoding is designed for data where there are relatively
few nonprintable characters; the base64 encoding scheme available via the
:mod:`base64` module is more compact if there are many such characters, as when
sending a graphics file.

.. function:: decode(input, output[,header])

   Decode the contents of the *input* file and write the resulting decoded binary
   data to the *output* file. *input* and *output* must either be file objects or
   objects that mimic the file object interface. *input* will be read until
   ``input.readline()`` returns an empty string. If the optional argument *header*
   is present and true, underscore will be decoded as space. This is used to decode
   "Q"-encoded headers as described in :rfc:`1522`: "MIME (Multipurpose Internet
   Mail Extensions) Part Two: Message Header Extensions for Non-ASCII Text".


.. function:: encode(input, output, quotetabs)

   Encode the contents of the *input* file and write the resulting quoted-printable
   data to the *output* file. *input* and *output* must either be file objects or
   objects that mimic the file object interface. *input* will be read until
   ``input.readline()`` returns an empty string. *quotetabs* is a flag which
   controls whether to encode embedded spaces and tabs; when true it encodes such
   embedded whitespace, and when false it leaves them unencoded.  Note that spaces
   and tabs appearing at the end of lines are always encoded, as per :rfc:`1521`.


.. function:: decodestring(s[,header])

   Like :func:`decode`, except that it accepts a source string and returns the
   corresponding decoded string.


.. function:: encodestring(s[, quotetabs])

   Like :func:`encode`, except that it accepts a source string and returns the
   corresponding encoded string.  *quotetabs* is optional (defaulting to 0), and is
   passed straight through to :func:`encode`.


.. seealso::

   Module :mod:`mimify`
      General utilities for processing of MIME messages.

   Module :mod:`base64`
      Encode and decode MIME base64 data

