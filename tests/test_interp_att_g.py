#!/usr/bin/env python
# coding=utf-8
from interp_att_g import InterpAttG
from tests.base import InkscapeExtensionTestMixin, TestCase


class InterpAttGBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = InterpAttG
        self.e = self.effect()
