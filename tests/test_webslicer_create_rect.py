#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from webslicer_create_rect import WebSlicer_CreateRect


class TestWebSlicerCreateRectBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = WebSlicer_CreateRect
