#!/usr/bin/env python
# coding=utf-8
from extrude import Extrude
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyleAndPath

class ExtrudeBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Extrude
    comparisons = [('--id=p1', '--id=p2')]
    compare_filters = [CompareOrderIndependentStyleAndPath()]
