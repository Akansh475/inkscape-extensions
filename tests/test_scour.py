#!/usr/bin/env python

from unittest import TestCase
import unittest
from output_scour import *

class ScourBasicTests(TestCase):
    def test_working(self):
        obj = ScourInkscape()

        input = "tests/data/svg/default-inkscape-SVG.svg"
        output = self.temp_file(suffix='.svg')
        output_expected = "tests/data/svg/default-inkscape-SVG_scoured.svg"

        obj.run(['--output', output, input])

        with open(output_expected, 'rb') as f:
            self.assertEqual(obj.document, f.read())

if __name__ == '__main__':
    unittest.main()
