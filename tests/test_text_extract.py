# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_extract import Extract

class TestExtractBasic(InkscapeExtensionTestMixin, TestCase):
    effect_class = Extract
