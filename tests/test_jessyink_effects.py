#!/usr/bin/en
# coding=utf-8
from jessyInk_effects import JessyInk_Effects
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkEffectsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = JessyInk_Effects
