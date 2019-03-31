# coding=utf-8
from guillotine import Guillotine
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestGuillotineBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Guillotine
