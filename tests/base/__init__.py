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
Provide tests with the tools to test extensions.
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

from io import BytesIO
import xml.etree.ElementTree as xml

from unittest import TestCase as BaseCase
from inkex.base import InkscapeExtension

from .xmldiff import xmldiff
from .mock import MockCommandMixin

if False: # pylint: disable=using-constant-test
    from typing import Type, List
    from .filters import Compare

TEST_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

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

    @property
    def temp_dir(self):
        """Generate a temporary location to store files"""
        if self._temp_dir is None:
            self._temp_dir = tempfile.mkdtemp(prefix='inkex-tests-')
        if not os.path.isdir(self._temp_dir):
            raise IOError("The temporary directory has disappeared!")
        return self._temp_dir

    def temp_file(self, prefix='file-', template='{prefix}{name}{suffix}', suffix='.tmp'):
        """Generate the filename of a temporary file"""
        filename = template.format(prefix=prefix, suffix=suffix, name=uuid.uuid4().hex)
        return os.path.join(self.temp_dir, filename)

    @staticmethod
    def data_file(filename, *parts):
        """Provide a data file from a filename, can accept directories as arguments."""
        full_path = os.path.join(TEST_ROOT, 'data', filename, *parts)
        if not os.path.isfile(full_path):
            raise IOError("Can't find test data file: {}".format(full_path))
        return full_path

    @property
    def root_dir(self):
        """Return the full path to the extensions directory"""
        return os.path.abspath(os.path.join(TEST_ROOT, '..'))

    @property
    def empty_svg(self):
        """Returns a common minimal svg file"""
        return self.data_file('svg', 'default-inkscape-SVG.svg')

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
        output = BytesIO()
        effect.test_output = output
        effect.run(args, output=output)

        if os.environ.get('FAIL_ON_DEPRICATION', False):
            warnings = getattr(effect, 'warned_about', set())
            effect.warned_about = set()  # reset for next test
            self.assertFalse(warnings, "Deprecated API is still being used!")

        return effect


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
            self.assertTrue(ret, "SVG Output Difference: {} <- {}".format(
                outfile,
                xml.tostring(xml_a.getroot()).decode('utf-8')))
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
        opstr = re.sub(r'[^\w-]', '__', '__'.join(args).replace(self.temp_dir, 'TMP_DIR'))
        if opstr:
            if len(opstr) > 127:
                # avoid filename-too-long error
                opstr = hashlib.md5(opstr.encode('latin1')).hexdigest()
            opstr = '__' + opstr
        return self.data_file("refs", "{}{}.out".format(effect_name, opstr))
