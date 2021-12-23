:mod:`urllib` --- Open arbitrary resources by URL
=================================================

.. module:: urllib
   :synopsis: Open an arbitrary network resource by URL (requires sockets).

.. note::
    The :mod:`urllib` module has been split into parts and renamed in
    Python 3 to :mod:`urllib.request`, :mod:`urllib.parse`,
    and :mod:`urllib.error`. The :term:`2to3` tool will automatically adapt
    imports when converting your sources to Python 3.
    Also note that the :func:`urllib.request.urlopen` function in Python 3 is
    equivalent to :func:`urllib2.urlopen` and that :func:`urllib.urlopen` has
    been removed.

.. index::
   single: WWW
   single: World Wide Web
   single: URL

This module provides a high-level interface for fetching data across the World
Wide Web.  In particular, the :func:`urlopen` function is similar to the
built-in function :func:`open`, but accepts Universal Resource Locators (URLs)
instead of filenames.  Some restrictions apply --- it can only open URLs for
reading, and no seek operations are available.

.. seealso::

    The `Requests package <http://docs.python-requests.org/>`_
    is recommended for a higher-level HTTP client interface.

.. versionchanged:: 2.7.9

    For HTTPS URIs, :mod:`urllib` performs all the neccessary certificate and hostname checks by default.

.. warning::

    For Python versions earlier than 2.7.9, urllib does not attempt to validate the server certificates of HTTPS URIs. Use at your own risk!


High-level interface
--------------------

.. function:: urlopen(url[, data[, proxies[, context]]])

   Open a network object denoted by a URL for reading.  If the URL does not
   have a scheme identifier, or if it has :file:`file:` as its scheme
   identifier, this opens a local file (without :term:`universal newlines`);
   otherwise it opens a socket to a server somewhere on the network.  If the
   connection cannot be made the :exc:`IOError` exception is raised.  If all
   went well, a file-like object is returned.  This supports the following
   methods: :meth:`read`, :meth:`readline`, :meth:`readlines`, :meth:`fileno`,
   :meth:`close`, :meth:`info`, :meth:`getcode` and :meth:`geturl`.  It also
   has proper support for the :term:`iterator` protocol. One caveat: the
   :meth:`read` method, if the size argument is omitted or negative, may not
   read until the end of the data stream; there is no good way to determine
   that the entire stream from a socket has been read in the general case.

   Except for the :meth:`info`, :meth:`getcode` and :meth:`geturl` methods,
   these methods have the same interface as for file objects --- see section
   :ref:`bltin-file-objects` in this manual.  (It is not a built-in file object,
   however, so it can't be used at those few places where a true built-in file
   object is required.)

   .. index:: module: mimetools

   The :meth:`info` method returns an instance of the class
   :class:`mimetools.Message` containing meta-information associated with the
   URL.  When the method is HTTP, these headers are those returned by the server
   at the head of the retrieved HTML page (including Content-Length and
   Content-Type).  When the method is FTP, a Content-Length header will be
   present if (as is now usual) the server passed back a file length in response
   to the FTP retrieval request. A Content-Type header will be present if the
   MIME type can be guessed.  When the method is local-file, returned headers
   will include a Date representing the file's last-modified time, a
   Content-Length giving file size, and a Content-Type containing a guess at the
   file's type. See also the description of the :mod:`mimetools` module.

   The :meth:`geturl` method returns the real URL of the page.  In some cases, the
   HTTP server redirects a client to another URL.  The :func:`urlopen` function
   handles this transparently, but in some cases the caller needs to know which URL
   the client was redirected to.  The :meth:`geturl` method can be used to get at
   this redirected URL.

   The :meth:`getcode` method returns the HTTP status code that was sent with the
   response, or ``None`` if the URL is no HTTP URL.

   If the *url* uses the :file:`http:` scheme identifier, the optional *data*
   argument may be given to specify a ``POST`` request (normally the request type
   is ``GET``).  The *data* argument must be in standard
   :mimetype:`application/x-www-form-urlencoded` format; see the :func:`urlencode`
   function below.

   The :func:`urlopen` function works transparently with proxies which do not
   require authentication.  In a Unix or Windows environment, set the
   :envvar:`http_proxy`, or :envvar:`ftp_proxy` environment variables to a URL that
   identifies the proxy server before starting the Python interpreter.  For example
   (the ``'%'`` is the command prompt)::

      % http_proxy="http://www.someproxy.com:3128"
      % export http_proxy
      % python
      ...

   The :envvar:`no_proxy` environment variable can be used to specify hosts which
   shouldn't be reached via proxy; if set, it should be a comma-separated list
   of hostname suffixes, optionally with ``:port`` appended, for example
   ``cern.ch,ncsa.uiuc.edu,some.host:8080``.

   In a Windows environment, if no proxy environment variables are set, proxy
   settings are obtained from the registry's Internet Settings section.

   .. index:: single: Internet Config

   In a Mac OS X  environment, :func:`urlopen` will retrieve proxy information
   from the OS X System Configuration Framework, which can be managed with
   Network System Preferences panel.


   Alternatively, the optional *proxies* argument may be used to explicitly specify
   proxies.  It must be a dictionary mapping scheme names to proxy URLs, where an
   empty dictionary causes no proxies to be used, and ``None`` (the default value)
   causes environmental proxy settings to be used as discussed above.  For
   example::

      # Use http://www.someproxy.com:3128 for HTTP proxying
      proxies = {'http': 'http://www.someproxy.com:3128'}
      filehandle = urllib.urlopen(some_url, proxies=proxies)
      # Don't use any proxies
      filehandle = urllib.urlopen(some_url, proxies={})
      # Use proxies from environment - both versions are equivalent
      filehandle = urllib.urlopen(some_url, proxies=None)
      filehandle = urllib.urlopen(some_url)

   Proxies which require authentication for use are not currently supported;
   this is considered an implementation limitation.

   The *context* parameter may be set to a :class:`ssl.SSLContext` instance to
   configure the SSL settings that are used if :func:`urlopen` makes a HTTPS
   connection.

   .. versionchanged:: 2.3
      Added the *proxies* support.

   .. versionchanged:: 2.6
      Added :meth:`getcode` to returned object and support for the
      :envvar:`no_proxy` environment variable.

   .. versionchanged:: 2.7.9
      The *context* parameter was added. All the neccessary certificate and hostname checks are done by default.

   .. deprecated:: 2.6
      The :func:`urlopen` function has been removed in Python 3 in favor
      of :func:`urllib2.urlopen`.


.. function:: urlretrieve(url[, filename[, reporthook[, data]]])

   Copy a network object denoted by a URL to a local file, if necessary. If the URL
   points to a local file, or a valid cached copy of the object exists, the object
   is not copied.  Return a tuple ``(filename, headers)`` where *filename* is the
   local file name under which the object can be found, and *headers* is whatever
   the :meth:`info` method of the object returned by :func:`urlopen` returned (for
   a remote object, possibly cached). Exceptions are the same as for
   :func:`urlopen`.

   The second argument, if present, specifies the file location to copy to (if
   absent, the location will be a tempfile with a generated name). The third
   argument, if present, is a hook function that will be called once on
   establishment of the network connection and once after each block read
   thereafter.  The hook will be passed three arguments; a count of blocks
   transferred so far, a block size in bytes, and the total size of the file.  The
   third argument may be ``-1`` on older FTP servers which do not return a file
   size in response to a retrieval request.

   If the *url* uses the :file:`http:` scheme identifier, the optional *data*
   argument may be given to specify a ``POST`` request (normally the request type
   is ``GET``).  The *data* argument must in standard
   :mimetype:`application/x-www-form-urlencoded` format; see the :func:`urlencode`
   function below.

   .. versionchanged:: 2.5
      :func:`urlretrieve` will raise :exc:`ContentTooShortError` when it detects that
      the amount of data available  was less than the expected amount (which is the
      size reported by a  *Content-Length* header). This can occur, for example, when
      the  download is interrupted.

      The *Content-Length* is treated as a lower bound: if there's more data  to read,
      :func:`urlretrieve` reads more data, but if less data is available,  it raises
      the exception.

      You can still retrieve the downloaded data in this case, it is stored  in the
      :attr:`content` attribute of the exception instance.

      If no *Content-Length* header was supplied, :func:`urlretrieve` can not check
      the size of the data it has downloaded, and just returns it.  In this case you
      just have to assume that the download was successful.


.. data:: _urlopener

   The public functions :func:`urlopen` and :func:`urlretrieve` create an instance
   of the :class:`FancyURLopener` class and use it to perform their requested
   actions.  To override this functionality, programmers can create a subclass of
   :class:`URLopener` or :class:`FancyURLopener`, then assign an instance of that
   class to the ``urllib._urlopener`` variable before calling the desired function.
   For example, applications may want to specify a different
   :mailheader:`User-Agent` header than :class:`URLopener` defines.  This can be
   accomplished with the following code::

      import urllib

      class AppURLopener(urllib.FancyURLopener):
          version = "App/1.7"

      urllib._urlopener = AppURLopener()


.. function:: urlcleanup()

   Clear the cache that may have been built up by previous calls to
   :func:`urlretrieve`.


Utility functions
-----------------

.. function:: quote(string[, safe])

   Replace special characters in *string* using the ``%xx`` escape. Letters,
   digits, and the characters ``'_.-'`` are never quoted. By default, this
   function is intended for quoting the path section of the URL. The optional
   *safe* parameter specifies additional characters that should not be quoted
   --- its default value is ``'/'``.

   Example: ``quote('/~connolly/')`` yields ``'/%7econnolly/'``.


.. function:: quote_plus(string[, safe])

   Like :func:`quote`, but also replaces spaces by plus signs, as required for
   quoting HTML form values when building up a query string to go into a URL.
   Plus signs in the original string are escaped unless they are included in
   *safe*.  It also does not have *safe* default to ``'/'``.


.. function:: unquote(string)

   Replace ``%xx`` escapes by their single-character equivalent.

   Example: ``unquote('/%7Econnolly/')`` yields ``'/~connolly/'``.


.. function:: unquote_plus(string)

   Like :func:`unquote`, but also replaces plus signs by spaces, as required for
   unquoting HTML form values.


.. function:: urlencode(query[, doseq])

   Convert a mapping object or a sequence of two-element tuples to a
   "percent-encoded" string, suitable to pass to :func:`urlopen` above as the
   optional *data* argument.  This is useful to pass a dictionary of form
   fields to a ``POST`` request.  The resulting string is a series of
   ``key=value`` pairs separated by ``'&'`` characters, where both *key* and
   *value* are quoted using :func:`quote_plus` above.  When a sequence of
   two-element tuples is used as the *query* argument, the first element of
   each tuple is a key and the second is a value. The value element in itself
   can be a sequence and in that case, if the optional parameter *doseq* is
   evaluates to ``True``, individual ``key=value`` pairs separated by ``'&'`` are
   generated for each element of the value sequence for the key.  The order of
   parameters in the encoded string will match the order of parameter tuples in
   the sequence. The :mod:`urlparse` module provides the functions
   :func:`parse_qs` and :func:`parse_qsl` which are used to parse query strings
   into Python data structures.


.. function:: pathname2url(path)

   Convert the pathname *path* from the local syntax for a path to the form used in
   the path component of a URL.  This does not produce a complete URL.  The return
   value will already be quoted using the :func:`quote` function.


.. function:: url2pathname(path)

   Convert the path component *path* from a percent-encoded URL to the local syntax for a
   path.  This does not accept a complete URL.  This function uses :func:`unquote`
   to decode *path*.


.. function:: getproxies()

   This helper function returns a dictionary of scheme to proxy server URL
   mappings. It scans the environment for variables named ``<scheme>_proxy``,
   in case insensitive way, for all operating systems first, and when it cannot
   find it, looks for proxy information from Mac OSX System Configuration for
   Mac OS X and Windows Systems Registry for Windows.
   If both lowercase and uppercase environment variables exist (and disagree),
   lowercase is preferred.

   .. note::

      If the environment variable ``REQUEST_METHOD`` is set, which usually
      indicates your script is running in a CGI environment, the environment
      variable ``HTTP_PROXY`` (uppercase ``_PROXY``) will be ignored. This is
      because that variable can be injected by a client using the "Proxy:" HTTP
      header. If you need to use an HTTP proxy in a CGI environment, either use
      ``ProxyHandler`` explicitly, or make sure the variable name is in
      lowercase (or at least the ``_proxy`` suffix).

.. note::
    urllib also exposes certain utility functions like splittype, splithost and
    others parsing URL into various components. But it is recommended to use
    :mod:`urlparse` for parsing URLs rather than using these functions directly.
    Python 3 does not expose these helper functions from :mod:`urllib.parse`
    module.


URL Opener objects
------------------

.. class:: URLopener([proxies[, context[, **x509]]])

   Base class for opening and reading URLs.  Unless you need to support opening
   objects using schemes other than :file:`http:`, :file:`ftp:`, or :file:`file:`,
   you probably want to use :class:`FancyURLopener`.

   By default, the :class:`URLopener` class sends a :mailheader:`User-Agent` header
   of ``urllib/VVV``, where *VVV* is the :mod:`urllib` version number.
   Applications can define their own :mailheader:`User-Agent` header by subclassing
   :class:`URLopener` or :class:`FancyURLopener` and setting the class attribute
   :attr:`version` to an appropriate string value in the subclass definition.

   The optional *proxies* parameter should be a dictionary mapping scheme names to
   proxy URLs, where an empty dictionary turns proxies off completely.  Its default
   value is ``None``, in which case environmental proxy settings will be used if
   present, as discussed in the definition of :func:`urlopen`, above.

   The *context* parameter may be a :class:`ssl.SSLContext` instance.  If given,
   it defines the SSL settings the opener uses to make HTTPS connections.

   Additional keyword parameters, collected in *x509*, may be used for
   authentication of the client when using the :file:`https:` scheme.  The keywords
   *key_file* and *cert_file* are supported to provide an  SSL key and certificate;
   both are needed to support client authentication.

   :class:`URLopener` objects will raise an :exc:`IOError` exception if the server
   returns an error code.

   .. method:: open(fullurl[, data])

      Open *fullurl* using the appropriate protocol.  This method sets up cache and
      proxy information, then calls the appropriate open method with its input
      arguments.  If the scheme is not recognized, :meth:`open_unknown` is called.
      The *data* argument has the same meaning as the *data* argument of
      :func:`urlopen`.


   .. method:: open_unknown(fullurl[, data])

      Overridable interface to open unknown URL types.


   .. method:: retrieve(url[, filename[, reporthook[, data]]])

      Retrieves the contents of *url* and places it in *filename*.  The return value
      is a tuple consisting of a local filename and either a
      :class:`mimetools.Message` object containing the response headers (for remote
      URLs) or ``None`` (for local URLs).  The caller must then open and read the
      contents of *filename*.  If *filename* is not given and the URL refers to a
      local file, the input filename is returned.  If the URL is non-local and
      *filename* is not given, the filename is the output of :func:`tempfile.mktemp`
      with a suffix that matches the suffix of the last path component of the input
      URL.  If *reporthook* is given, it must be a function accepting three numeric
      parameters.  It will be called after each chunk of data is read from the
      network.  *reporthook* is ignored for local URLs.

      If the *url* uses the :file:`http:` scheme identifier, the optional *data*
      argument may be given to specify a ``POST`` request (normally the request type
      is ``GET``).  The *data* argument must in standard
      :mimetype:`application/x-www-form-urlencoded` format; see the :func:`urlencode`
      function below.


   .. attribute:: version

      Variable that specifies the user agent of the opener object.  To get
      :mod:`urllib` to tell servers that it is a particular user agent, set this in a
      subclass as a class variable or in the constructor before calling the base
      constructor.


.. class:: FancyURLopener(...)

   :class:`FancyURLopener` subclasses :class:`URLopener` providing default handling
   for the following HTTP response codes: 301, 302, 303, 307 and 401.  For the 30x
   response codes listed above, the :mailheader:`Location` header is used to fetch
   the actual URL.  For 401 response codes (authentication required), basic HTTP
   authentication is performed.  For the 30x response codes, recursion is bounded
   by the value of the *maxtries* attribute, which defaults to 10.

   For all other response codes, the method :meth:`http_error_default` is called
   which you can override in subclasses to handle the error appropriately.

   .. note::

      According to the letter of :rfc:`2616`, 301 and 302 responses to POST requests
      must not be automatically redirected without confirmation by the user.  In
      reality, browsers do allow automatic redirection of these responses, changing
      the POST to a GET, and :mod:`urllib` reproduces this behaviour.

   The parameters to the constructor are the same as those for :class:`URLopener`.

   .. note::

      When performing basic authentication, a :class:`FancyURLopener` instance calls
      its :meth:`prompt_user_passwd` method.  The default implementation asks the
      users for the required information on the controlling terminal.  A subclass may
      override this method to support more appropriate behavior if needed.

   The :class:`FancyURLopener` class offers one additional method that should be
   overloaded to provide the appropriate behavior:

   .. method:: prompt_user_passwd(host, realm)

      Return information needed to authenticate the user at the given host in the
      specified security realm.  The return value should be a tuple, ``(user,
      password)``, which can be used for basic authentication.

      The implementation prompts for this information on the terminal; an application
      should override this method to use an appropriate interaction model in the local
      environment.

.. exception:: ContentTooShortError(msg[, content])

   This exception is raised when the :func:`urlretrieve` function detects that the
   amount of the downloaded data is less than the  expected amount (given by the
   *Content-Length* header). The :attr:`content` attribute stores the downloaded
   (and supposedly truncated) data.

   .. versionadded:: 2.5


:mod:`urllib` Restrictions
--------------------------

  .. index::
     pair: HTTP; protocol
     pair: FTP; protocol

* Currently, only the following protocols are supported: HTTP, (versions 0.9 and
  1.0),  FTP, and local files.

* The caching feature of :func:`urlretrieve` has been disabled until I find the
  time to hack proper processing of Expiration time headers.

* There should be a function to query whether a particular URL is in the cache.

* For backward compatibility, if a URL appears to point to a local file but the
  file can't be opened, the URL is re-interpreted using the FTP protocol.  This
  can sometimes cause confusing error messages.

* The :func:`urlopen` and :func:`urlretrieve` functions can cause arbitrarily
  long delays while waiting for a network connection to be set up.  This means
  that it is difficult to build an interactive Web client using these functions
  without using threads.

  .. index::
     single: HTML
     pair: HTTP; protocol
     module: htmllib

* The data returned by :func:`urlopen` or :func:`urlretrieve` is the raw data
  returned by the server.  This may be binary data (such as an image), plain text
  or (for example) HTML.  The HTTP protocol provides type information in the reply
  header, which can be inspected by looking at the :mailheader:`Content-Type`
  header.  If the returned data is HTML, you can use the module :mod:`htmllib` to
  parse it.

  .. index:: single: FTP

* The code handling the FTP protocol cannot differentiate between a file and a
  directory.  This can lead to unexpected behavior when attempting to read a URL
  that points to a file that is not accessible.  If the URL ends in a ``/``, it is
  assumed to refer to a directory and will be handled accordingly.  But if an
  attempt to read a file leads to a 550 error (meaning the URL cannot be found or
  is not accessible, often for permission reasons), then the path is treated as a
  directory in order to handle the case when a directory is specified by a URL but
  the trailing ``/`` has been left off.  This can cause misleading results when
  you try to fetch a file whose read permissions make it inaccessible; the FTP
  code will try to read it, fail with a 550 error, and then perform a directory
  listing for the unreadable file. If fine-grained control is needed, consider
  using the :mod:`ftplib` module, subclassing :class:`FancyURLopener`, or changing
  *_urlopener* to meet your needs.

* This module does not support the use of proxies which require authentication.
  This may be implemented in the future.

  .. index:: module: urlparse

* Although the :mod:`urllib` module contains (undocumented) routines to parse
  and unparse URL strings, the recommended interface for URL manipulation is in
  module :mod:`urlparse`.


.. _urllib-examples:

Examples
--------

Here is an example session that uses the ``GET`` method to retrieve a URL
containing parameters::

   >>> import urllib
   >>> params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
   >>> f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query?%s" % params)
   >>> print f.read()

The following example uses the ``POST`` method instead::

   >>> import urllib
   >>> params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
   >>> f = urllib.urlopen("http://www.musi-cal.com/cgi-bin/query", params)
   >>> print f.read()

The following example uses an explicitly specified HTTP proxy, overriding
environment settings::

   >>> import urllib
   >>> proxies = {'http': 'http://proxy.example.com:8080/'}
   >>> opener = urllib.FancyURLopener(proxies)
   >>> f = opener.open("http://www.python.org")
   >>> f.read()

The following example uses no proxies at all, overriding environment settings::

   >>> import urllib
   >>> opener = urllib.FancyURLopener({})
   >>> f = opener.open("http://www.python.org/")
   >>> f.read()

