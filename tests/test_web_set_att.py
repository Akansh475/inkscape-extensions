# coding=utf-8
from web_set_att import InkWebTransmitAtt
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestWebSetAttBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = InkWebTransmitAtt
    comparisons = [('--id=p1', '--id=r3')]
