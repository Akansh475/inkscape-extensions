# coding=utf-8

import os

from dxf_input import DxfInput

from tests.base import TEST_ROOT, ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy


class TestDxfInputBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    compare_file = 'r12.dxf'
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [()]
    effect = DxfInput

    def _apply_compare_filters(self, data):
        """Remove the full pathnames"""
        data = super(TestDxfInputBasic, self)._apply_compare_filters(data)
        return data.replace(os.path.join(TEST_ROOT, 'data') + '/', '')

    def setUp(self):
        self.e = self.effect()
