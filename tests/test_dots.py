#!/usr/bin/env python
# coding=utf-8

import unittest

from dots import Dots
from tests.base import InkscapeExtensionTestMixin, TestCase


class DotsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Dots
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
