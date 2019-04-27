# coding=utf-8

import os

from dxf_input import DxfInput

from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy


class TestDxfInputBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    compare_file = 'r12.dxf'
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [()]
    effect_class = DxfInput

    def _apply_compare_filters(self, data):
        """Remove the full pathnames"""
        data = super(TestDxfInputBasic, self)._apply_compare_filters(data)
        return data.replace((self.datadir() + '/').encode('utf-8'), b'')
