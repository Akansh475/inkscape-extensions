# coding=utf-8
from empty_video import EmptyVideo
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestEmptyVideoBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = EmptyVideo
    comparisons = [('--size=Custom', '-w', '10', '-z', '10')]
