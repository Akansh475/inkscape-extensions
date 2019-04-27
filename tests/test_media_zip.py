# coding=utf-8
from media_zip import CompressedMediaOutput
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareSize

class CmoBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = CompressedMediaOutput
    compare_filters = [CompareSize()]
    comparisons = [()]
