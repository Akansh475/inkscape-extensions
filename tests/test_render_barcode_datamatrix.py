# coding=utf-8
from render_barcode_datamatrix import DataMatrix
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle

class TestDataMatrixBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = DataMatrix
    compare_filters = [CompareOrderIndependentStyle()]
