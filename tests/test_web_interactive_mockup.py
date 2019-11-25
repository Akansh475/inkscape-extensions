# coding=utf-8
from web_interactive_mockup import InkWebIMockup
from inkex.tester import ComparisonMixin, TestCase

class TestInkWebInteractiveMockupBasic(ComparisonMixin, TestCase):
    effect_class = InkWebIMockup
    comparisons = [('--id=p1', '--id=r3')]
