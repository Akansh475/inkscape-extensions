# coding=utf-8
from generate_voronoi import Pattern
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestPatternBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = Pattern
