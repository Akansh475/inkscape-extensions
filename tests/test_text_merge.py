#!/usr/bin/env python
from text_merge import Merge
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class TestMergeBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Merge
