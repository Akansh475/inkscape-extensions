#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from webslicer_effect import WebSlicer_Effect


class TestWebSlicerEffectBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = WebSlicer_Effect
