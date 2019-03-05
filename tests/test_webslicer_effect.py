#!/usr/bin/env python
# coding=utf-8
from webslicer_effect import WebSlicer_Effect
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestWebSlicerEffectBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = WebSlicer_Effect
        self.e = self.effect()


