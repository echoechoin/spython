# -*- coding: utf-8 -*-

import mimetypes
import StringIO
import unittest
import sys

from test import test_support

# Tell it we don't know about external files:
mimetypes.knownfiles = []
mimetypes.inited = False
mimetypes._default_mime_types()


class MimeTypesTestCase(unittest.TestCase):
    def setUp(self):
        self.db = mimetypes.MimeTypes()

    def test_default_data(self):
        eq = self.assertEqual
        eq(self.db.guess_type("foo.html"), ("text/html", None))
        eq(self.db.guess_type("foo.tgz"), ("application/x-tar", "gzip"))
        eq(self.db.guess_type("foo.tar.gz"), ("application/x-tar", "gzip"))
        eq(self.db.guess_type("foo.tar.Z"), ("application/x-tar", "compress"))
        eq(self.db.guess_type("foo.tar.bz2"), ("application/x-tar", "bzip2"))
        eq(self.db.guess_type("foo.tar.xz"), ("application/x-tar", "xz"))

    def test_data_urls(self):
        eq = self.assertEqual
        guess_type = self.db.guess_type
        eq(guess_type("data:,thisIsTextPlain"), ("text/plain", None))
        eq(guess_type("data:;base64,thisIsTextPlain"), ("text/plain", None))
        eq(guess_type("data:text/x-foo,thisIsTextXFoo"), ("text/x-foo", None))

    def test_file_parsing(self):
        eq = self.assertEqual
        sio = StringIO.StringIO("x-application/x-unittest pyunit\n")
        self.db.readfp(sio)
        eq(self.db.guess_type("foo.pyunit"),
           ("x-application/x-unittest", None))
        eq(self.db.guess_extension("x-application/x-unittest"), ".pyunit")

    def test_non_standard_types(self):
        eq = self.assertEqual
        # First try strict
        eq(self.db.guess_type('foo.xul', strict=True), (None, None))
        eq(self.db.guess_extension('image/jpg', strict=True), None)
        # And then non-strict
        eq(self.db.guess_type('foo.xul', strict=False), ('text/xul', None))
        eq(self.db.guess_extension('image/jpg', strict=False), '.jpg')

    def test_guess_all_types(self):
        eq = self.assertEqual
        unless = self.assertTrue
        # First try strict.  Use a set here for testing the results because if
        # test_urllib2 is run before test_mimetypes, global state is modified
        # such that the 'all' set will have more items in it.
        all = set(self.db.guess_all_extensions('text/plain', strict=True))
        unless(all >= set(['.bat', '.c', '.h', '.ksh', '.pl', '.txt']))
        # And now non-strict
        all = self.db.guess_all_extensions('image/jpg', strict=False)
        all.sort()
        eq(all, ['.jpg'])
        # And now for no hits
        all = self.db.guess_all_extensions('image/jpg', strict=True)
        eq(all, [])


@unittest.skipUnless(sys.platform.startswith("win"), "Windows only")
class Win32MimeTypesTestCase(unittest.TestCase):
    def setUp(self):
        # ensure all entries actually come from the Windows registry
        self.original_types_map = mimetypes.types_map.copy()
        mimetypes.types_map.clear()

    def tearDown(self):
        # restore default settings
        mimetypes.types_map.clear()
        mimetypes.types_map.update(self.original_types_map)

    def test_registry_parsing(self):
        # the original, minimum contents of the MIME database in the
        # Windows registry is undocumented AFAIK.
        # Use file types that should *always* exist:
        eq = self.assertEqual
        mimetypes.init()
        db = mimetypes.MimeTypes()
        eq(db.guess_type("foo.txt"), ("text/plain", None))
        eq(db.guess_type("image.jpg"), ("image/jpeg", None))
        eq(db.guess_type("image.png"), ("image/png", None))

    def test_non_latin_extension(self):
        import _winreg

        class MockWinreg(object):
            def __getattr__(self, name):
                if name == 'EnumKey':
                    return lambda key, i: _winreg.EnumKey(key, i) + "\xa3"
                elif name == 'OpenKey':
                    return lambda key, name: _winreg.OpenKey(key, name.rstrip("\xa3"))
                elif name == 'QueryValueEx':
                    return lambda subkey, label: (u'текст/простой' , _winreg.REG_SZ)
                return getattr(_winreg, name)

        mimetypes._winreg = MockWinreg()
        try:
            # this used to throw an exception if registry contained non-Latin
            # characters in extensions (issue #9291)
            mimetypes.init()
        finally:
            mimetypes._winreg = _winreg

    def test_non_latin_type(self):
        import _winreg

        class MockWinreg(object):
            def __getattr__(self, name):
                if name == 'QueryValueEx':
                    return lambda subkey, label: (u'текст/простой', _winreg.REG_SZ)
                return getattr(_winreg, name)

        mimetypes._winreg = MockWinreg()
        try:
            # this used to throw an exception if registry contained non-Latin
            # characters in content types (issue #9291)
            mimetypes.init()
        finally:
            mimetypes._winreg = _winreg

    def test_type_map_values(self):
        import _winreg

        class MockWinreg(object):
            def __getattr__(self, name):
                if name == 'QueryValueEx':
                    return lambda subkey, label: (u'text/plain', _winreg.REG_SZ)
                return getattr(_winreg, name)

        mimetypes._winreg = MockWinreg()
        try:
            mimetypes.init()
            self.assertTrue(isinstance(mimetypes.types_map.values()[0], str))
        finally:
            mimetypes._winreg = _winreg

    def test_registry_read_error(self):
        import _winreg

        class MockWinreg(object):
            def OpenKey(self, key, name):
                if key != _winreg.HKEY_CLASSES_ROOT:
                    raise WindowsError(5, "Access is denied")
                return _winreg.OpenKey(key, name)
            def __getattr__(self, name):
                return getattr(_winreg, name)

        mimetypes._winreg = MockWinreg()
        try:
            mimetypes.init()
        finally:
            mimetypes._winreg = _winreg

def test_main():
    test_support.run_unittest(MimeTypesTestCase,
        Win32MimeTypesTestCase
    )


if __name__ == "__main__":
    test_main()
