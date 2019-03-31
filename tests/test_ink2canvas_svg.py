#!/usr/bin/en
# coding=utf-8
from ink2canvas import Ink2Canvas
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentLines

class Ink2CanvasBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Ink2Canvas
    compare_filters = [CompareOrderIndependentLines()]
