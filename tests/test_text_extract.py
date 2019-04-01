# coding=utf-8
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from text_extract import Extract

class TestExtractBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Extract
