# coding=utf-8
from guillotine import Guillotine
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestGuillotineBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Guillotine
