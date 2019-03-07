#!/usr/bin/env python
# coding=utf-8
from guides_creator import GuidesCreator
from tests.base import InkscapeExtensionTestMixin, TestCase


class GuidesCreatorBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GuidesCreator
        self.e = self.effect()
