# coding=utf-8
from web_interactive_mockup import InkWebIMockup
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestInkWebInteractiveMockupBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = InkWebIMockup
    comparisons = [('--id=p1', '--id=r3')]
