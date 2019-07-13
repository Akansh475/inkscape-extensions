# coding=utf-8
from interp import Interp
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class InterpBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Interp
    comparisons = [
        ('--id=a', '--id=b', '--id=c', '--id=d'),
        ('--method=1', '--id=a', '--id=b', '--id=c', '--id=d'),
    ]
    compare_file = 'svg/interp_stars.svg'
