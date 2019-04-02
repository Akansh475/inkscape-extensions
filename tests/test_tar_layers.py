# coding=utf-8
from tar_layers import LayersOutput
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareSize

class LayersOutputBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = LayersOutput
    compare_filters = [CompareSize()]
