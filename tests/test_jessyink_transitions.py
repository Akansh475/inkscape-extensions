# coding=utf-8
from jessyInk_transitions import JessyInk_Transitions
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class JessyInkTransitionsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = JessyInk_Transitions
    comparisons = [('--layerName', 'Slide2')]
