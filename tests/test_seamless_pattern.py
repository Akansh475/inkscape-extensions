#!/usr/bin/env python
# coding=utf-8

import unittest

from seamless_pattern import C
from tests.base import InkscapeExtensionTestMixin, TestCase


class SeamlessPatternBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
