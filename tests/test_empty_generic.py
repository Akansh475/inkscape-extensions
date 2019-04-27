# coding=utf-8
from empty_generic import GenericTemplate
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class TestGenericTemplateBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = GenericTemplate
    compare_filters = [CompareNumericFuzzy()]
