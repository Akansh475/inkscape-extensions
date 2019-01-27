#!/usr/bin/env python
#
# Unit test file for ../markers_strokepaint.py
# Revision history:
#  * 2012-01-27 (jazzynico): checks defaulf parameters and file handling.
#

from tests.base import TestCase
import unittest
from markers_strokepaint import MarkerStrokePaintEffect

class StrokeColorBasicTest(TestCase):
    effect = MarkerStrokePaintEffect

    def test_empty_defs(self):
        e = MarkerStrokePaintEffect()
        e.run([self.data_file('svg', 'default-plain-SVG.svg')])

if __name__ == '__main__':
    unittest.main()
