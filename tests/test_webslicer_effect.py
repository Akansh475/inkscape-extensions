#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from webslicer_effect import WebSlicer_Effect


class TestWebSlicerEffectBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = WebSlicer_Effect
        self.e = self.effect()
