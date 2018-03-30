#!/usr/bin/env python
#
# Unit test file for ../markers_strokepaint.py
# Revision history:
#  * 2012-01-27 (jazzynico): checks defaulf parameters and file handling.
#

from tests.base import TestCase, test_support
from markers_strokepaint import *

class StrokeColorBasicTest(TestCase):
    effect = MyEffect

    def test_empty_defs(self):
        e = MyEffect()
        e.affect([self.data_file('svg', 'default-plain-SVG.svg')], False)

if __name__ == '__main__':
    test_support.run_unittest(StrokeColorBasicTest)
