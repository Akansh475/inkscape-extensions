# coding=utf-8
from jessyInk_summary import Summary
from inkex.tester import ComparisonMixin, TestCase

class JessyInkSummaryTest(ComparisonMixin, TestCase):
    stderr_protect = False
    effect_class = Summary
