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
Written to test the coding of generating barcodes.
"""

import unittest

from render_barcode import InsertBarcode
from tests.base import InkscapeExtensionTestMixin, TestCase


class InsertBarcodeBasicTest(InkscapeExtensionTestMixin, TestCase):
    """Render Barcode"""

    def setUp(self):
        self.effect = InsertBarcode
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
