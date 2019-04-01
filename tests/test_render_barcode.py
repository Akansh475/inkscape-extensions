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
from render_barcode import InsertBarcode
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class InsertBarcodeBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = InsertBarcode
    comparisons = [
        ('--type', 'Ean2', '--text', '55'),
        ('--type', 'Code93', '--text', '3332222'),
        ('--type', 'Upce', '--text', '123456'),
    ]
