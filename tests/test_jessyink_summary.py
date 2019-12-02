# coding=utf-8
from jessyInk_summary import Summary
from inkex.tester import ComparisonMixin, TestCase

class JessyInkSummaryBasicTest(ComparisonMixin, TestCase):
    effect_class = Summary
