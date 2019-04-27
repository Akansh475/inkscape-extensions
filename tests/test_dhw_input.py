# coding=utf-8

from dhw_input import DhwInput

from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy


class TestDxfInput(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DhwInput
    compare_file = [
        'dhw/PAGE_001.DHW',
        'dhw/PGLT_161.DHW',
        'dhw/PGLT_162.DHW',
        'dhw/PGLT_163.DHW',
    ]
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [()]
