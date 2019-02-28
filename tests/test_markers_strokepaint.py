#!/usr/bin/env python
# coding=utf-8
#
# Unit test file for ../markers_strokepaint.py
# Revision history:
#  * 2012-01-27 (jazzynico): checks defaulf parameters and file handling.
#

from tests.base import InkscapeExtensionTestMixin, TestCase
import unittest
from markers_strokepaint import MarkerStrokePaintEffect
import inkex

class MarkerStrokePaintBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = MarkerStrokePaintEffect
        self.e = self.effect()

    def test_empty_defs(self):
        e = MarkerStrokePaintEffect()
        e.run([self.data_file('svg', 'minimal-blank.svg')])
        self.assertTrue (0 < len(e.document.xpath('//svg:defs', namespaces=inkex.NSS)))

    def test_basic(self):
        args = [
            '--id=dimension'
            , self.data_file('svg', 'markers.svg')]
        e = MarkerStrokePaintEffect()
        e.run(args)
        old_markers = e.original_document.xpath('//svg:defs//svg:marker', namespaces=inkex.NSS)
        new_markers = e.document.xpath('//svg:defs//svg:marker', namespaces=inkex.NSS)
        self.assertTrue (len (old_markers) == 2)
        self.assertTrue (len (new_markers) == 4)

if __name__ == '__main__':
    unittest.main()
