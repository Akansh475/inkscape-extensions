#!/usr/bin/env python
from webslicer_create_rect import WebSlicer_CreateRect
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestWebSlicerCreateRectBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = WebSlicer_CreateRect
