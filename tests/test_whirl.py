#!/usr/bin/env python
# coding=utf-8

import unittest

from tests.base import InkscapeExtensionTestMixin, TestCase
from whirl import Whirl


class WhirlBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Whirl
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
