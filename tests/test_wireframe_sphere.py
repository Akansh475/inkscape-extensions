# coding=utf-8
from wireframe_sphere import WireframeSphere
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareOrderIndependentStyle

class TestWireframeSphereBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = WireframeSphere
    compare_filters = [CompareNumericFuzzy(), CompareOrderIndependentStyle()]
