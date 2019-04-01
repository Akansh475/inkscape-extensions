# coding=utf-8
from render_gear_rack import RackGear
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class TestRackGearBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = RackGear
    compare_filters = [CompareOrderIndependentStyle()]
