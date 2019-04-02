# coding=utf-8
from wireframe_sphere import WireframeSphere
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy

class TestWireframeSphereBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = WireframeSphere
    compare_filters = [CompareNumericFuzzy()]
