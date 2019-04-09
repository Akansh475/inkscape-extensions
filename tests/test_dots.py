# coding=utf-8
from dots import Dots
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class DotsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Dots
    comparisons = [('--id=p1', '--id=r3')]
