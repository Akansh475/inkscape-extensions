# coding=utf-8
#
# Copyright (C) 2018 Martin Owens
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
Provide tests with some base utility.
"""
from __future__ import absolute_import, print_function, unicode_literals

import os
import shutil
import tempfile
import uuid
from unittest import TestCase as BaseCase

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

    def __init__(self, *args, **kw):
        super(TestCase, self).__init__(*args, **kw)
        self.temp_dir = None
        self.effect = NoExtension

    def tearDown(self):
        if self.temp_dir and os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def temp_file(self, prefix='file-', template='{prefix}{name}{suffix}', suffix='.tmp'):
        """Generate the filename of a temporary file"""
        if not self.temp_dir:
            self.temp_dir = tempfile.mkdtemp(prefix='inkex-tests-')
        if not os.path.isdir(self.temp_dir):
            raise IOError("The temporary directory has disappeared!")
        filename = template.format(prefix=prefix, suffix=suffix, name=uuid.uuid4().hex)
        return os.path.join(self.temp_dir, filename)

    @staticmethod
    def data_file(filename, *parts):
        """Provide a data file from a filename, can accept directories as arguments."""
        full_path = os.path.join(TEST_ROOT, 'data', filename, *parts)
        if not os.path.isfile(full_path):
            raise IOError("Can't find test data file: {}".format(filename))
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

        effect.run(args)

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
