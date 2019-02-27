#!/usr/bin/env python
# coding=utf-8

import unittest

from coloreffect import ColorEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class ColorEffectBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = ColorEffect
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
