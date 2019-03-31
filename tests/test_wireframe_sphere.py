#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from wireframe_sphere import WireframeSphere


class TestWireframeSphereBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = WireframeSphere
