# coding=utf-8
from tar_layers import LayersOutput
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareSize

class LayersOutputBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = LayersOutput
    compare_filters = [CompareSize()]
