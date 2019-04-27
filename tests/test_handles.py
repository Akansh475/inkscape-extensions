#!/usr/bin/env python
# coding=utf-8
from handles import Handles
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class HandlesBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Handles
