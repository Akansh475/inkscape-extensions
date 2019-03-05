#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from text_merge import Merge


class TestMergeBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Merge
        self.e = self.effect()
