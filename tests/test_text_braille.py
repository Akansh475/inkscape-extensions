# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_braille import Braille

class TestBrailleBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = Braille
