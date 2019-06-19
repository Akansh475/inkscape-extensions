# coding=utf-8
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from text_extract import Extract
import pytest


@pytest.mark.skip(reason="Does not produce correct output")
class TestExtractBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Extract
