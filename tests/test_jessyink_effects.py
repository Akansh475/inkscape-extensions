#!/usr/bin/en
# coding=utf-8
from jessyInk_effects import JessyInk_Effects
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class JessyInkEffectsBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = JessyInk_Effects
