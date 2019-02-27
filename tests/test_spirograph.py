#!/usr/bin/env python
# coding=utf-8

import unittest

from spirograph import Spirograph
from tests.base import InkscapeExtensionTestMixin, TestCase


class SpirographBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Spirograph
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
