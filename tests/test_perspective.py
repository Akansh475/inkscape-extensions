#!/usr/bin/env python
# coding=utf-8
#
# Unit test file for ../perspective.py
# Revision history:
#  * 2012-01-28 (jazzynico): first working version (only checks the extension
#    with the default parameters).
#
from perspective import Project
from tests.base import InkscapeExtensionTestMixin, TestCase


class PerspectiveBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Project
        self.e = self.effect()
