#!/usr/bin/env python

import unittest

from edge3d import Edge3d
from tests.base import InkscapeExtensionTestMixin, TestCase


class Edge3dBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Edge3d
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
