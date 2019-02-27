#!/usr/bin/env python
# coding=utf-8

import unittest

from extrude import Extrude
from tests.base import InkscapeExtensionTestMixin, TestCase


class ExtrudeBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Extrude
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
