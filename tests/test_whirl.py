# coding=utf-8
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from whirl import Whirl

class WhirlBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Whirl
