#!/usr/bin/en
# coding=utf-8
from jessyInk_autoTexts import JessyInk_AutoTexts
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkAutoTextsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_AutoTexts
    comparisons = [('--autoText', 'slideTitle', '--id', 't1')]
