# coding=utf-8
from empty_video import EmptyVideo
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestEmptyVideoBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = EmptyVideo
    comparisons = [('--size=Custom', '-w', '10', '-z', '10')]
