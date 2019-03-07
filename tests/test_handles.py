#!/usr/bin/env python
# coding=utf-8
from handles import Handles
from tests.base import InkscapeExtensionTestMixin, TestCase


class HandlesBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Handles
        self.e = self.effect()
