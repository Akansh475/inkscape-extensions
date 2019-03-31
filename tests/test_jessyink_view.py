# coding=utf-8
from jessyInk_view import JessyInk_Effects
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkEffectsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Effects
    comparisons = [('--id=r3', '--viewOrder=1')]
