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

import sys
import uuid
import shutil
import tempfile
from os import path
from unittest import TestCase as BaseCase

# python 2.7 and python 3.5 support
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from test import test_support
except ImportError:
    # pylint: disable=no-name-in-module
    from test import support as test_support

TEST_ROOT = path.abspath(path.dirname(path.dirname(__file__)))


class StdRedirect(object): # pylint: disable=too-few-public-methods
    """Capture printed output, or provide standard input

    with StdRedirect('stdout') as out:
        print("expected")
        str(out) == 'expected'

    with StdRedirect('stdin', 'data') as inp:
        sys.stdin.read() == 'data'
        imp += 'more data arrived'
    """
    def __init__(self, name='stdout', initial=None):
        self.name = name
        self.std = getattr(sys, self.name)
        self.str = StringIO(initial)

    def __enter__(self):
        setattr(sys, self.name, self.str)
        return self

    def __str__(self):
        self.str.seek(0)
        return self.str.read()

    def __repr__(self):
        return "<StdRedirect {}>".format(self.name)

    def __iadd__(self, data):
        self.str.seek(0, mode=2)
        self.str.write(data)
        self.str.seek(0, mode=1)

    def __exit__(self, kind, value, traceback):
        setattr(sys, self.name, self.std)


class TestCase(BaseCase):
    """
    Base class for all effects tests, provides access to data_files and test_without_parameters
    """
    def __init__(self, *args, **kw):
        super(TestCase, self).__init__(*args, **kw)
        self.temp_dir = None

    def tearDown(self):
        if self.temp_dir and path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def temp_file(self, prefix='file-', template='{prefix}{name}{suffix}', suffix='.tmp'):
        """Generate the filename of a temporary file"""
        if not self.temp_dir:
            self.temp_dir = tempfile.mkdtemp(prefix='inkex-tests-')
        if not path.isdir(self.temp_dir):
            raise IOError("The temporary directory has disappeared!")
        filename = template.format(prefix=prefix, suffix=suffix, name=uuid.uuid4().hex)
        return path.join(self.temp_dir, filename)

    @staticmethod
    def data_file(filename, *parts):
        """Provide a data file from a filename, can accept directories as arguments."""
        full_path = path.join(TEST_ROOT, 'data', filename, *parts)
        if not path.isfile(full_path):
            raise IOError("Can't find test data file: {}".format(filename))
        return full_path

    @property
    def root_dir(self):
        """Return the full path to the extensions directory"""
        return path.abspath(path.join(TEST_ROOT, '..'))

    @property
    def empty_svg(self):
        """Returns a common minimal svg file"""
        return self.data_file('svg', 'default-inkscape-SVG.svg')

    def assertEffectEmpty(self, effect, **kwargs): # pylint: disable=invalid-name
        """Assert calling effect without any arguments"""
        args = ['--{}={}'.format(*kw) for kw in kwargs.items()]
        effect().run([self.empty_svg] + args)
        warnings = getattr(effect, 'warned_about', set())
       # self.assertFalse(warnings, "Depricated API is still being used!")

