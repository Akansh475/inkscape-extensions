# coding=utf-8
from straightseg import SegmentStraightener
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace

class SegmentStraightenerBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = SegmentStraightener
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]
