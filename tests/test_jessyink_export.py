# coding=utf-8
from jessyInk_export import JessyInkExport
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareSize

class JessyInkExportBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = JessyInkExport
    comparisons = [()]
    compare_filters = [CompareSize()]
