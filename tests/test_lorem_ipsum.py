# coding=utf-8
from lorem_ipsum import LorumImpsum
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class LorumImpsumBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = LorumImpsum
    comparisons = [()]
