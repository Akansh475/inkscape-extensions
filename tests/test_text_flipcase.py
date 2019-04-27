# coding=utf-8
from text_flipcase import FlipCase
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestFlipCaseBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = FlipCase
