#!/usr/bin/env python
from webslicer_export import WebSlicer_Export
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestWebSlicerExportBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = WebSlicer_Export

    @property
    def comparisons(self):
        return [('--dir', self.temp_dir)]
