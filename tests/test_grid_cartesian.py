#!/usr/bin/env python
# coding=utf-8

import unittest

from grid_cartesian import GridCartesian
from tests.base import InkscapeExtensionTestMixin, TestCase


class GridPolarBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GridCartesian
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
