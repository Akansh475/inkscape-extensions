#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from triangle import Triangle


class TriangleBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Triangle
        self.e = self.effect()
