#!/usr/bin/env python
# coding=utf-8
#
# Unit test file for ../markers_strokepaint.py
# Revision history:
#  * 2012-01-27 (jazzynico): checks defaulf parameters and file handling.
#

import unittest

from markers_strokepaint import MarkerStrokePaintEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class StrokeColorBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = MarkerStrokePaintEffect
        self.e = self.effect()

    def test_empty_defs(self):
        self.e.run([self.data_file('svg', 'default-plain-SVG.svg')])


if __name__ == '__main__':
    unittest.main()
