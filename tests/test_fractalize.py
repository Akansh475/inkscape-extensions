#!/usr/bin/env python
# coding=utf-8

import unittest

from fractalize import PathFractalize
from tests.base import InkscapeExtensionTestMixin, TestCase


class PathFractalizeBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PathFractalize
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
