# coding=utf-8
from media_zip import CompressedMediaOutput
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareSize

class CmoBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = CompressedMediaOutput
    compare_filters = [CompareSize()]
    comparisons = [()]
