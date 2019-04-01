# coding=utf-8
from text_flipcase import FlipCase
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestFlipCaseBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = FlipCase
