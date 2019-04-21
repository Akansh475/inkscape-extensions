# coding=utf-8
from printing_marks import PrintingMarks
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace, \
    CompareOrderIndependentStyle

class PrintingMarksBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PrintingMarks
    compare_filters = [
        CompareNumericFuzzy(),
        CompareWithPathSpace(),
        CompareOrderIndependentStyle(),
    ]
