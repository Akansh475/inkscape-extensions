# coding=utf-8
from fractalize import PathFractalize
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class PathFractalizeBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = PathFractalize
    comparisons = [('--id=p1', '--id=p2')]
