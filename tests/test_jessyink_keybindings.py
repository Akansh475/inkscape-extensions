# coding=utf-8
from jessyInk_keyBindings import JessyInk_CustomKeyBindings
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkCustomKeyBindingsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_CustomKeyBindings
