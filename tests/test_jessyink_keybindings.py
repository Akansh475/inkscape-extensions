# coding=utf-8
from jessyInk_keyBindings import KeyBindings
from inkex.tester import ComparisonMixin, TestCase

class JessyInkCustomKeyBindingsBasicTest(ComparisonMixin, TestCase):
    effect_class = KeyBindings
