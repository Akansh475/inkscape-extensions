#!/usr/bin/env python

import unittest

from grid_polar import GridPolar
from tests.base import InkscapeExtensionTestMixin, TestCase


class GridPolarBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GridPolar
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
