#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from webslicer_export import WebSlicer_Export


class TestWebSlicerExportBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = WebSlicer_Export
