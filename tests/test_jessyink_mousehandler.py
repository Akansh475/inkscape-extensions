# coding=utf-8
from jessyInk_mouseHandler import JessyInk_CustomMouseHandler
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class JessyInkCustomMouseHandlerBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = JessyInk_CustomMouseHandler
