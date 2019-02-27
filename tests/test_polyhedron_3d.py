#!/usr/bin/env python
# coding=utf-8

import unittest

from polyhedron_3d import Poly3D
from tests.base import InkscapeExtensionTestMixin, TestCase


class Poly3DBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Poly3D
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
