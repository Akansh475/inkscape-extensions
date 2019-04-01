# coding=utf-8
import os

from output_scour import ScourInkscape
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class ScourBasicTests(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = ScourInkscape
    comparisons = [()]
