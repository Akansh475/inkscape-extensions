#!/usr/bin/env python
# coding=utf-8

import unittest

from chardataeffect import CharDataEffect
from tests.base import InkscapeExtensionTestMixin, TestCase


class CharDataBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = CharDataEffect
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
