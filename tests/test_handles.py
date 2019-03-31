#!/usr/bin/env python
# coding=utf-8
from handles import Handles
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class HandlesBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = Handles
