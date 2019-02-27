#!/usr/bin/env python
# coding=utf-8

import unittest

from rtree import RTreeTurtle
from tests.base import InkscapeExtensionTestMixin, TestCase


class RTreeTurtleBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = RTreeTurtle
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
