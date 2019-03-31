# coding=utf-8
from empty_generic import GenericTemplate
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy

class TestGenericTemplateBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = GenericTemplate
    compare_filters = [CompareNumericFuzzy()]
