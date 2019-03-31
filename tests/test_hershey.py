# coding=utf-8
from hershey import Hershey
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy

class TestHersheyBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Hershey
    comparisons = [('--fontface=timesr', )]
    compare_filters = [CompareNumericFuzzy()]
