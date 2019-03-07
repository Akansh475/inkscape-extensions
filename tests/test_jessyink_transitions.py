#!/usr/bin/en
# coding=utf-8
from jessyInk_transitions import JessyInk_Transitions
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkTransitionsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_Transitions
        self.e = self.effect()
