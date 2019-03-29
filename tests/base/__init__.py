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
import shutil
import tempfile
import hashlib
import uuid

from io import StringIO
import xml.etree.ElementTree as xml

from unittest import TestCase as BaseCase

from .xmldiff import xmldiff

TEST_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class NoExtension(object):  # pylint: disable=too-few-public-methods
    """Test case must specify 'self.effect' to assertEffect."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(self.__doc__)

    def run(self, *args, **kwargs):
        """Fake run"""
        pass


class TestCase(BaseCase):
    """
    Base class for all effects tests, provides access to data_files and test_without_parameters
    """
    effect = NoExtension

    def __init__(self, *args, **kw):
        super(TestCase, self).__init__(*args, **kw)
        self._temp_dir = None

    def tearDown(self):
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
        effect = kwargs.pop('effect', self.effect)()

        args = [self.data_file(*filename)] if filename else [self.empty_svg]  # pylint: disable=no-value-for-parameter
        args += kwargs.pop('args', [])
        args += ['--{}={}'.format(*kw) for kw in kwargs.items()]

        # Output is redirected to this string io buffer
        output = StringIO()
        effect.test_output = output
        effect.run(args, output=output)

        if os.environ.get('FAIL_ON_DEPRICATION', False):
            warnings = getattr(effect, 'warned_about', set())
            effect.warned_about = set()  # reset for next test
            self.assertFalse(warnings, "Deprecated API is still being used!")

        return effect


class InkscapeExtensionTestMixin(object):
    def test_default_settings_cause_no_exception(self):
        if self.effect is None:
            self.skipTest('self.effect is not defined for this this test')
        self.e = self.effect()
        args = [self.empty_svg]
        self.e.run(args)


class ComparisonMixin(object):
    """
    Add comparison tests to any existing test suite.
    """
    compare_file = 'ref_test.svg'
    compare_filters = []
    comparisons = [
        (),
        ('--id=p1', '--id=r3'),
    ]

    def test_all_comparisons(self):
        """Testing all comparisons"""
        for args in self.comparisons:
            self.assertCompare(
                self.compare_file,
                self.get_compare_outfile(args),
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

        data_a = self._apply_compare_filters(effect.test_output.getvalue())
        with open(outfile, 'r') as fhl:
            data_b = self._apply_compare_filters(fhl.read())

        if data_a.startswith('<') and data_b.startswith('<'):
            # Compare two svg files
            xml_a = xml.parse(StringIO(data_a))
            xml_b = xml.parse(StringIO(data_b))
            # Late importing
            ret = xmldiff(xml_a.getroot(), xml_b.getroot())
            self.assertTrue(ret, "SVG Output Difference: {}".format(
                xml.tostring(xml_a.getroot()).decode('utf-8')))
        else:
            # compare any content (non svg)
            self.assertEqual(data_a, data_b)

    def _apply_compare_filters(self, data):
        for cfilter in self.compare_filters:
            data = cfilter(data)
        return data

    def get_compare_outfile(self, args):
        """Generate an output file for the arguments given"""
        effect_name = self.effect.__module__
        opstr = re.sub(r'[^\w-]', '__', '__'.join(args).replace(self.temp_dir, 'TMP_DIR'))
        if opstr:
            if len(opstr) > 127:
                # avoid filename-too-long error
                opstr = hashlib.md5(opstr.encode('latin1')).hexdigest()
            opstr = '__' + opstr
        return self.data_file("refs", "{}{}.out".format(effect_name, opstr))
