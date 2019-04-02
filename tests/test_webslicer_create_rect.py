#!/usr/bin/env python
from webslicer_create_rect import WebSlicer_CreateRect
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestWebSlicerCreateRectBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = WebSlicer_CreateRect
