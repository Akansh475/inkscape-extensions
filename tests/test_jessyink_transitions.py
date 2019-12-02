# coding=utf-8
from jessyInk_transitions import Transitions
from inkex.tester import ComparisonMixin, TestCase

class JessyInkTransitionsBasicTest(ComparisonMixin, TestCase):
    effect_class = Transitions
    comparisons = [('--layerName', 'Slide2')]
