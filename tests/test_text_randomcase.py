# coding=utf-8
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from text_randomcase import RandomCase

class TestRandomCaseBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = RandomCase
    comparisons = [()]
