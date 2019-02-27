#!/usr/bin/env python
# coding=utf-8

import unittest

from output_scour import ScourInkscape
from tests.base import InkscapeExtensionTestMixin, TestCase


class ScourBasicTests(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ScourInkscape
        self.e = self.effect()

    def test_working(self):
        input = "tests/data/svg/default-inkscape-SVG.svg"
        output = self.temp_file(suffix='.svg')
        output_expected = "tests/data/svg/default-inkscape-SVG_scoured.svg"

        self.e.run(['--output', output, input])

        with open(output_expected, 'rb') as f:
            self.assertEqual(self.e.document, f.read())


if __name__ == '__main__':
    unittest.main()
