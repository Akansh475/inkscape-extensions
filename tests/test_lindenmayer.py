# coding=utf-8
from lindenmayer import LSystem
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class LSystemBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = LSystem
