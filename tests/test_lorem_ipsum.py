# coding=utf-8
from lorem_ipsum import LorumImpsum
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class LorumImpsumBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = LorumImpsum
    comparisons = [()]
