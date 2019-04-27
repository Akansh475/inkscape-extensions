# coding=utf-8
from empty_icon import EmptyIcon
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestEmptyIconBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = EmptyIcon
