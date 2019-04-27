# coding=utf-8
import os

from output_scour import ScourInkscape
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class ScourBasicTests(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = ScourInkscape
    comparisons = [()]
