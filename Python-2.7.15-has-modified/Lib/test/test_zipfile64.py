# Tests of the full ZIP64 functionality of zipfile
# The test_support.requires call is the only reason for keeping this separate
# from test_zipfile
from test import test_support

# XXX(nnorwitz): disable this test by looking for extra largfile resource
# which doesn't exist.  This test takes over 30 minutes to run in general
# and requires more disk space than most of the buildbots.
test_support.requires(
        'extralargefile',
        'test requires loads of disk-space bytes and a long time to run'
    )

# We can test part of the module without zlib.
try:
    import zlib
except ImportError:
    zlib = None

import zipfile, os, unittest
import time
import sys

from tempfile import TemporaryFile

from test.test_support import TESTFN, run_unittest

TESTFN2 = TESTFN + "2"

# How much time in seconds can pass before we print a 'Still working' message.
_PRINT_WORKING_MSG_INTERVAL = 5 * 60

class TestsWithSourceFile(unittest.TestCase):
    def setUp(self):
        # Create test data.
        # xrange() is important here -- don't want to create immortal space
        # for a million ints.
        line_gen = ("Test of zipfile line %d." % i for i in xrange(1000000))
        self.data = '\n'.join(line_gen)

        # And write it to a file.
        fp = open(TESTFN, "wb")
        fp.write(self.data)
        fp.close()

    def zipTest(self, f, compression):
        # Create the ZIP archive.
        zipfp = zipfile.ZipFile(f, "w", compression, allowZip64=True)

        # It will contain enough copies of self.data to reach about 6GB of
        # raw data to store.
        filecount = 6*1024**3 // len(self.data)

        next_time = time.time() + _PRINT_WORKING_MSG_INTERVAL
        for num in range(filecount):
            zipfp.writestr("testfn%d" % num, self.data)
            # Print still working message since this test can be really slow
            if next_time <= time.time():
                next_time = time.time() + _PRINT_WORKING_MSG_INTERVAL
                print >>sys.__stdout__, (
                   '  zipTest still writing %d of %d, be patient...' %
                   (num, filecount))
                sys.__stdout__.flush()
        zipfp.close()

        # Read the ZIP archive
        zipfp = zipfile.ZipFile(f, "r", compression)
        for num in range(filecount):
            self.assertEqual(zipfp.read("testfn%d" % num), self.data)
            # Print still working message since this test can be really slow
            if next_time <= time.time():
                next_time = time.time() + _PRINT_WORKING_MSG_INTERVAL
                print >>sys.__stdout__, (
                   '  zipTest still reading %d of %d, be patient...' %
                   (num, filecount))
                sys.__stdout__.flush()
        zipfp.close()

    def testStored(self):
        # Try the temp file first.  If we do TESTFN2 first, then it hogs
        # gigabytes of disk space for the duration of the test.
        with TemporaryFile() as f:
            self.zipTest(f, zipfile.ZIP_STORED)
            self.assertFalse(f.closed)
        self.zipTest(TESTFN2, zipfile.ZIP_STORED)

    @unittest.skipUnless(zlib, "requires zlib")
    def testDeflated(self):
        # Try the temp file first.  If we do TESTFN2 first, then it hogs
        # gigabytes of disk space for the duration of the test.
        with TemporaryFile() as f:
            self.zipTest(f, zipfile.ZIP_DEFLATED)
            self.assertFalse(f.closed)
        self.zipTest(TESTFN2, zipfile.ZIP_DEFLATED)

    def tearDown(self):
        for fname in TESTFN, TESTFN2:
            if os.path.exists(fname):
                os.remove(fname)


class OtherTests(unittest.TestCase):
    def testMoreThan64kFiles(self):
        # This test checks that more than 64k files can be added to an archive,
        # and that the resulting archive can be read properly by ZipFile
        zipf = zipfile.ZipFile(TESTFN, mode="w", allowZip64=True)
        zipf.debug = 100
        numfiles = (1 << 16) * 3/2
        for i in xrange(numfiles):
            zipf.writestr("foo%08d" % i, "%d" % (i**3 % 57))
        self.assertEqual(len(zipf.namelist()), numfiles)
        zipf.close()

        zipf2 = zipfile.ZipFile(TESTFN, mode="r")
        self.assertEqual(len(zipf2.namelist()), numfiles)
        for i in xrange(numfiles):
            self.assertEqual(zipf2.read("foo%08d" % i), "%d" % (i**3 % 57))
        zipf2.close()

    def testMoreThan64kFilesAppend(self):
        zipf = zipfile.ZipFile(TESTFN, mode="w", allowZip64=False)
        zipf.debug = 100
        numfiles = (1 << 16) - 1
        for i in range(numfiles):
            zipf.writestr("foo%08d" % i, "%d" % (i**3 % 57))
        self.assertEqual(len(zipf.namelist()), numfiles)
        with self.assertRaises(zipfile.LargeZipFile):
            zipf.writestr("foo%08d" % numfiles, b'')
        self.assertEqual(len(zipf.namelist()), numfiles)
        zipf.close()

        zipf = zipfile.ZipFile(TESTFN, mode="a", allowZip64=False)
        zipf.debug = 100
        self.assertEqual(len(zipf.namelist()), numfiles)
        with self.assertRaises(zipfile.LargeZipFile):
            zipf.writestr("foo%08d" % numfiles, b'')
        self.assertEqual(len(zipf.namelist()), numfiles)
        zipf.close()

        zipf = zipfile.ZipFile(TESTFN, mode="a", allowZip64=True)
        zipf.debug = 100
        self.assertEqual(len(zipf.namelist()), numfiles)
        numfiles2 = (1 << 16) * 3//2
        for i in range(numfiles, numfiles2):
            zipf.writestr("foo%08d" % i, "%d" % (i**3 % 57))
        self.assertEqual(len(zipf.namelist()), numfiles2)
        zipf.close()

        zipf2 = zipfile.ZipFile(TESTFN, mode="r")
        self.assertEqual(len(zipf2.namelist()), numfiles2)
        for i in range(numfiles2):
            self.assertEqual(zipf2.read("foo%08d" % i), "%d" % (i**3 % 57))
        zipf2.close()

    def tearDown(self):
        test_support.unlink(TESTFN)
        test_support.unlink(TESTFN2)

def test_main():
    run_unittest(TestsWithSourceFile, OtherTests)

if __name__ == "__main__":
    test_main()
