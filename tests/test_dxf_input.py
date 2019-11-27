# coding=utf-8

from dxf_input import DxfInput

from inkex.tester import ComparisonMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class TestDxfInputBasic(ComparisonMixin, TestCase):
    compare_file = ['io/test_r12.dxf', 'io/test_r14.dxf']
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [()]
    effect_class = DxfInput

    def _apply_compare_filters(self, data):
        """Remove the full pathnames"""
        data = super(TestDxfInputBasic, self)._apply_compare_filters(data)
        return data.replace((self.datadir() + '/').encode('utf-8'), b'')

