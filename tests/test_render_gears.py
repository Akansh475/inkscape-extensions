# coding=utf-8
from render_gears import Gears
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class GearsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Gears
    compare_filters = [CompareOrderIndependentStyle()]
