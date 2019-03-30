# coding=utf-8
from empty_icon import EmptyIcon
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestEmptyIconBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = EmptyIcon
