#!/usr/bin/env python
# coding=utf-8

import unittest

from flatten import MyEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class MyEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = MyEffect
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
