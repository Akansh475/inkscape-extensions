#!/usr/bin/env python
# coding=utf-8

import unittest

from render_gears import Gears
from tests.base import InkscapeExtensionTestMixin, TestCase


class GearsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Gears
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
