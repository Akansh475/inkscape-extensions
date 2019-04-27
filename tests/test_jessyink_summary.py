# coding=utf-8
from jessyInk_summary import JessyInk_Summary
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkSummaryBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Summary
