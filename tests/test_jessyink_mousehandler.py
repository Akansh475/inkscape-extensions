# coding=utf-8
from jessyInk_mouseHandler import JessyInk_CustomMouseHandler
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class JessyInkCustomMouseHandlerBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_CustomMouseHandler
