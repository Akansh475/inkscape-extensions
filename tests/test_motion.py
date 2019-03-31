# coding=utf-8
from motion import Motion
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace

class MotionBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Motion
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]
