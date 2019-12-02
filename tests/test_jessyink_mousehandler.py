# coding=utf-8
from jessyInk_mouseHandler import MouseHandler
from inkex.tester import ComparisonMixin, TestCase

class JessyInkCustomMouseHandlerBasicTest(ComparisonMixin, TestCase):
    effect_class = MouseHandler
