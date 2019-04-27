# coding=utf-8
from empty_desktop import EmptyDesktop
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class TestEmptyDesktopBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = EmptyDesktop
    comparisons = [('--size=100x50', )]
