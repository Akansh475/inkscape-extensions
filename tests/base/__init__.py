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
import os

from unittest import TestCase as BaseCase

# python 2.7 and python 3.5 support
try:
    from test import test_support
except ImportError:
    from test import support as test_support

# Allow import of the extension code and modules
#sys.path.append('..')

TEST_ROOT = os.path.dirname(os.path.dirname(__file__))

class TestCase(BaseCase):
    effect = None

    @staticmethod
    def data_file(fn, *path):
        path = os.path.join(TEST_ROOT, 'data', fn, *path)
        if not os.path.isfile(path):
            raise IOError("Can't find test data file: {}".format(fn))
        return path

    @property
    def empty_svg(self):
        return self.data_file('svg', 'minimal-blank.svg')

    def test_without_parameters(self):
        if self.effect:
            self.effect().affect([self.empty_svg], False)

