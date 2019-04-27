# coding=utf-8
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from text_extract import Extract

class TestExtractBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Extract
