# coding=utf-8
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from text_randomcase import RandomCase

class TestRandomCaseBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = RandomCase
