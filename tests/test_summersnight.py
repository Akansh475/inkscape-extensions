# coding=utf-8
#
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#
from summersnight import Project
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy, CompareWithPathSpace

class EnvelopeBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Project
    comparisons = [('--id=p1', '--id=p2')]
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]
