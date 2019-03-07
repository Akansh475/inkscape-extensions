#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from wireframe_sphere import WireframeSphere


class TestWireframeSphereBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = WireframeSphere
        self.e = self.effect()
