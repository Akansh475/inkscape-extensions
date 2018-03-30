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

from collections import defaultdict
from tests.base import TestCase, test_support

from render_barcode import *

digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]

class InsertBarcodeBasicTest(TestCase):
    """Render Barcode"""
    data = defaultdict(list)

    @classmethod
    def setUpClass(cls):
        with open(cls.data_file('render_barcode.data'), 'r') as fhl:
            for line in fhl:
                (btype, text, code) = line.strip().split(':', 2)
                cls.data[btype].append((text, code))

    def test_render_barcode_ian5(self):
        """Barcode IAN5"""
        self.barcode_test('Ean5')

    def test_render_barcode_ian8(self):
        """Barcode IAN5"""
        self.barcode_test('Ean8')

    def test_render_barcode_ian13(self):
        """Barcode IAN5"""
        self.barcode_test('Ean13')

    def test_render_barcode_upca(self):
        """Barcode IAN5"""
        self.barcode_test('Upca')

    def test_render_barcode_upce(self):
        """Barcode UPCE"""
        self.barcode_test('Upce')

    def barcode_test(self, name):
        """Base module for all barcode testing"""
        for datum in self.data[name.lower()]:
            (text, code) = datum
            if not text or not code:
                continue
            coder = getBarcode(name, text=text)
            code2 = coder.encode( text )
            self.assertEqual(code, code2)


if __name__ == '__main__':
    test_support.run_unittest(InsertBarcodeBasicTest)

