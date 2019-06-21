#!/usr/bin/env python
# coding=utf-8
from handles import Handles
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class HandlesBasicTest(ComparisonMixin, TestCase):
    effect_class = Handles
    compare_file = 'ref_curves.svg'
    comparisons = (
        ('--id=curve', '--id=quad'),
    )
