# coding=utf-8
from text_braille import Braille
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestBrailleBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Braille
