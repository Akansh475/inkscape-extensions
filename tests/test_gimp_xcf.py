#!/usr/bin/env python
"""
Unit test file for ../gimp_xcf.py
Revision history:
  * 2012-01-26 (jazzynico): checks defaulf parameters and file handling.
"""

from tests.base import TestCase
import unittest
from gimp_xcf import *

class GimpXCFBasicTest(TestCase):
    def _test_expected_file(self):
        """multilayered-test.svg provides 3 layers and a sublayer (all non empty)"""
        e = MyEffect()
        e.affect([self.data_file('svg', 'multilayered-test.svg')])
        #self.assertRaises(GimpXCFExpectedIOError, e.affect, args, False)

    def _test_empty_file(self):
        # empty-SVG.svg contains an emply svg element (no layer, no object).
        # The file must have at least one non empty layer and thus the
        # extension rejects it and send an error message.
        e = MyEffect()
        e.affect([self.data_file('svg', 'minimal-blank.svg')])
        self.assertEqual(e.valid, 0)

    def _test_empty_layer_file(self):
        # default-inkscape-SVG.svg is a copy of the default Inkscape
        # template, with one empty layer.
        # The file must have at least one non empty layer and thus the
        # extension rejects it and send an error message.
        e = MyEffect()
        e.affect([self.data_file('svg', 'default-inkscape-SVG.svg')])
        self.assertEqual(e.valid, 0)


if __name__ == '__main__':
    unittest.main()
