#!/usr/bin/env python
# coding=utf-8

import unittest

from lindenmayer import LSystem
from tests.base import InkscapeExtensionTestMixin, TestCase


class LSystemBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = LSystem
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
