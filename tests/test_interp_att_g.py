#!/usr/bin/env python
# coding=utf-8
from interp_att_g import InterpAttG
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class InterpAttGBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = InterpAttG
    comparisons = [('--id=layer1',)]
