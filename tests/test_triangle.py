#!/usr/bin/env python
from triangle import Triangle
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareOrderIndependentStyle

class TriangleBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Triangle
    compare_filters = [CompareNumericFuzzy(), CompareOrderIndependentStyle()]
