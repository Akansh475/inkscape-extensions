#!/usr/bin/env python
# coding=utf-8

import unittest

from interp import Interp
from tests.base import InkscapeExtensionTestMixin, TestCase


class InterpBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Interp
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
