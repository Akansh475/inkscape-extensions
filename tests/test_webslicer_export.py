#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from webslicer_export import WebSlicer_Export


class TestWebSlicerExportBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = WebSlicer_Export
        self.e = self.effect()
