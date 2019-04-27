# coding=utf-8
from jessyInk_keyBindings import JessyInk_CustomKeyBindings
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkCustomKeyBindingsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_CustomKeyBindings
