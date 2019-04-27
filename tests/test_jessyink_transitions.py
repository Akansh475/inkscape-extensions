# coding=utf-8
from jessyInk_transitions import JessyInk_Transitions
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class JessyInkTransitionsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Transitions
    comparisons = [('--layerName', 'Slide2')]
