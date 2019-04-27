# coding=utf-8
from jessyInk_view import JessyInk_Effects
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkEffectsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Effects
    comparisons = [('--id=r3', '--viewOrder=1')]
