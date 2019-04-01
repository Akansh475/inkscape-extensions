#!/usr/bin/env python
# coding=utf-8
#
# Unit test file for ../perspective.py
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#
from perspective import Project
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class PerspectiveBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Project
    comparisons = [('--id=p1', '--id=p2')]
