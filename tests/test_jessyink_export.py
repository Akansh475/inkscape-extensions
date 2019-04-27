# coding=utf-8
from jessyInk_export import JessyInkExport
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareSize

class JessyInkExportBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    compare_filters = [CompareSize()]
    effect_class = JessyInkExport
    comparisons = [()]
