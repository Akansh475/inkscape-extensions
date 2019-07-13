# coding=utf-8
#
# Copyright (C) 2018-2019 Martin Owens
#               2019 Thomas Holder
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110, USA.
#
"""
All extensions should come with tests, this package provides you will all the
tools you need in order to create tests and make sure your extension continues
to work with new versions of Inkscape, the Inkex python modules and other
python and non-python tools you may use.

Make sure your extension is a python extension and is using the `inkex.generic`
base classes. As these provide the greatest amount of functionality for testing.

You should start by creating a folder in your repository called `tests` with
an empty file inside called `__init__.py` to turn it into a module folder.

For each of your extensions, you should create a file called
`test_{myextension}.py` where the name reflects the name of your extension.

There are two types of tests:

    1. Full-process Comparison tests - These are tests which envoke your
           extension will various arguments and attempt to compare the
           output to a known good state. These are useful for testing
           that your extension would work, if it was used in Inkscape.

           Good example of writing comparison tests can be found in the
           inkscape core repository, each test which inherits from
           the ComparisonMixin class are running comparison tests.

    2. Unit tests - These are individual test functions which call out to
           specific functions within your extension. These are typical
           python unit testing and many good python documents exist
           to describe how to write them well. For examples here you
           can find the tests that test the inkex modules themsleves
           to be the most instructive.

Your tests will hit a cetain amount of code, this is called it's **coverage**
and the higher the coverage, the better your tests are at stretching all
the options and varients your code has.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import re
import sys
import shutil
import tempfile
import hashlib
import random
import uuid

from io import BytesIO, StringIO
import xml.etree.ElementTree as xml

from unittest import TestCase as BaseCase
from inkex.base import InkscapeExtension

from .xmldiff import xmldiff
from .mock import MockCommandMixin

if False: # pylint: disable=using-constant-test
    from typing import Type, List
    from .filters import Compare


class NoExtension(InkscapeExtension):  # pylint: disable=too-few-public-methods
    """Test case must specify 'self.effect_class' to assertEffect."""

    def __init__(self, *args, **kwargs): # pylint: disable=super-init-not-called
        raise NotImplementedError(self.__doc__)

    def run(self, args=None, output=None):
        """Fake run"""
        pass


class TestCase(MockCommandMixin, BaseCase):
    """
    Base class for all effects tests, provides access to data_files and test_without_parameters
    """
    effect_class = NoExtension # type: Type[InkscapeExtension]

    # If set to true, the output is not expected to be the stdout SVG document, but rather
    # text or a message sent to the stderr, this is highly weird. But sometimes happens.
    stderr_output = False

    def __init__(self, *args, **kw):
        super(TestCase, self).__init__(*args, **kw)
        self._temp_dir = None

    def setUp(self): # pylint: disable=invalid-name
        """Make sure every test is seeded the same way"""
        super(TestCase, self).setUp()
        try:
            # python3, with version 1 to get the same numbers
            # as in python2 during tests.
            random.seed(0x35f, version=1)
        except TypeError:
            # But of course this kwarg doesn't exist in python2
            random.seed(0x35f)

    def tearDown(self):
        super(TestCase, self).tearDown()
        if self._temp_dir and os.path.isdir(self._temp_dir):
            shutil.rmtree(self._temp_dir)

    @classmethod
    def __file__(cls):
        """Create a __file__ property which acts much like the module version"""
        return os.path.abspath(sys.modules[cls.__module__].__file__)

    @classmethod
    def _testdir(cls):
        """Get's the folder where the test exists (so data can be found)"""
        return os.path.dirname(cls.__file__())

    @classmethod
    def rootdir(cls):
        """Return the full path to the extensions directory"""
        return os.path.dirname(cls._testdir())

    @classmethod
    def datadir(cls):
        """Get the data directory (can be over-ridden if needed)"""
        return os.path.join(cls._testdir(), 'data')

    @property
    def tempdir(self):
        """Generate a temporary location to store files"""
        if self._temp_dir is None:
            self._temp_dir = tempfile.mkdtemp(prefix='inkex-tests-')
        if not os.path.isdir(self._temp_dir):
            raise IOError("The temporary directory has disappeared!")
        return self._temp_dir

    def temp_file(self, prefix='file-', template='{prefix}{name}{suffix}', suffix='.tmp'):
        """Generate the filename of a temporary file"""
        filename = template.format(prefix=prefix, suffix=suffix, name=uuid.uuid4().hex)
        return os.path.join(self.tempdir, filename)

    @classmethod
    def data_file(cls, filename, *parts):
        """Provide a data file from a filename, can accept directories as arguments."""
        full_path = os.path.join(cls.datadir(), filename, *parts)
        if not os.path.isfile(full_path):
            raise IOError("Can't find test data file: {}".format(full_path))
        return full_path

    @property
    def empty_svg(self):
        """Returns a common minimal svg file"""
        return self.data_file('svg', 'default-inkscape-SVG.svg')

    def assertAlmostTuple(self, found, expected, precision=8): # pylint: disable=invalid-name
        """
        Floating point results may vary with computer architecture; use
        assertAlmostEqual to allow a tolerance in the result.
        """
        self.assertEqual(len(found), len(expected))
        for fon, exp in zip(found, expected):
            self.assertAlmostEqual(fon, exp, precision)

    def assertEffectEmpty(self, effect, **kwargs):  # pylint: disable=invalid-name
        """Assert calling effect without any arguments"""
        self.assertEffect(effect=effect, **kwargs)

    def assertEffect(self, *filename, **kwargs):  # pylint: disable=invalid-name
        """Assert an effect, capturing the output to stdout.

           filename should point to a starting svg document, default is empty_svg
        """
        effect = kwargs.pop('effect', self.effect_class)()

        args = [self.data_file(*filename)] if filename else [self.empty_svg]  # pylint: disable=no-value-for-parameter
        args += kwargs.pop('args', [])
        args += ['--{}={}'.format(*kw) for kw in kwargs.items()]

        # Output is redirected to this string io buffer
        if self.stderr_output:
            output = StringIO()
            stderr, sys.stderr = sys.stderr, output
            try:
                effect.run(args, output=BytesIO())
            finally:
                sys.stderr = stderr
        else:
            output = BytesIO()
            effect.run(args, output=output)
        effect.test_output = output

        if os.environ.get('FAIL_ON_DEPRICATION', False):
            warnings = getattr(effect, 'warned_about', set())
            effect.warned_about = set()  # reset for next test
            self.assertFalse(warnings, "Deprecated API is still being used!")

        return effect

    def assertDeepAlmostEqual(self, first, second, places=7, msg=None, delta=None):
        if isinstance(first, (list, tuple)):
            assert len(first) == len(second)
            for (f, s) in zip(first, second):
                self.assertDeepAlmostEqual(f, s, places, msg, delta)
        else:
            self.assertAlmostEqual(first, second, places, msg, delta)


class InkscapeExtensionTestMixin(object):
    """Automatically setup self.effect for each test and test with an empty svg"""
    def setUp(self): # pylint: disable=invalid-name
        """Check if there's an effect_class set and create self.effect is it is"""
        super(InkscapeExtensionTestMixin, self).setUp()
        if self.effect_class is None:
            self.skipTest('self.effect_class is not defined for this this test')
        self.effect = self.effect_class()

    def test_default_settings(self):
        """Extension works with empty svg file"""
        self.effect.run([self.empty_svg])

class ComparisonMixin(object):
    """
    Add comparison tests to any existing test suite.
    """
    compare_file = 'ref_test.svg'
    compare_filters = [] # type: List[Compare]
    comparisons = [
        (),
        ('--id=p1', '--id=r3'),
    ]

    def test_all_comparisons(self):
        """Testing all comparisons"""
        if not isinstance(self.compare_file, (list, tuple)):
            self._test_comparisons(self.compare_file)
        else:
            for compare_file in self.compare_file:
                self._test_comparisons(
                    compare_file,
                    addout=os.path.basename(compare_file)
                )

    def _test_comparisons(self, compare_file, addout=None):
        for args in self.comparisons:
            self.assertCompare(
                compare_file,
                self.get_compare_outfile(args, addout),
                args,
            )

    def assertCompare(self, infile, outfile, args): #pylint: disable=invalid-name
        """
        Compare the output of a previous run against this one.

         - infile: The filename of the pre-proccessed svg (or other type of file)
         - outfile: The filename of the data we expect to get, if not set
                    the filename will be generated from the effect name and kwargs.
         - args: All the arguments to be passed to the effect run

        """
        effect = self.assertEffect(infile, args=args)

        if outfile is None:
            outfile = self.get_compare_outfile(args)

        if not os.path.isfile(outfile):
            raise IOError("Comparison file {} not found".format(outfile))

        data_a = effect.test_output.getvalue()
        if os.environ.get('EXPORT_COMPARE', False):
            with open(outfile + '.export', 'wb') as fhl:
                if sys.version_info[0] == 3 and isinstance(data_a, str):
                    data_a = data_a.encode('utf-8')
                fhl.write(data_a)
                print("Written output: {}.export".format(outfile))
        data_a = self._apply_compare_filters(data_a)

        with open(outfile, 'rb') as fhl:
            data_b = self._apply_compare_filters(fhl.read())

        if isinstance(data_a, bytes) and isinstance(data_b, bytes) \
            and data_a.startswith(b'<') and data_b.startswith(b'<'):
            # Compare two svg files
            xml_a = xml.parse(BytesIO(data_a))
            xml_b = xml.parse(BytesIO(data_b))
            # Late importing
            ret = xmldiff(xml_a.getroot(), xml_b.getroot())
            diff = xml.tostring(xml_a.getroot()).decode('utf-8')
            self.assertTrue(ret, "SVG Output Difference: {} <- {}".format(outfile, diff))
        else:
            # compare any content (non svg)
            self.assertEqual(data_a, data_b)

    def _apply_compare_filters(self, data):
        if sys.version_info[0] == 3 and isinstance(data, str):
            data = data.encode('utf-8')
        for cfilter in self.compare_filters:
            data = cfilter(data)
        return data

    def get_compare_outfile(self, args, addout=None):
        """Generate an output file for the arguments given"""
        effect_name = self.effect_class.__module__
        if addout is not None:
            args = list(args) + [str(addout)]
        opstr = '__'.join(args)\
                    .replace(self.tempdir, 'TMP_DIR')\
                    .replace(self.datadir(), 'DAT_DIR')
        opstr = re.sub(r'[^\w-]', '__', opstr)
        if opstr:
            if len(opstr) > 127:
                # avoid filename-too-long error
                opstr = hashlib.md5(opstr.encode('latin1')).hexdigest()
            opstr = '__' + opstr
        return self.data_file("refs", "{}{}.out".format(effect_name, opstr))
