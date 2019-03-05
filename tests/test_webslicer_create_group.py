#!/usr/bin/env python
# coding=utf-8
from tests.base import InkscapeExtensionTestMixin, TestCase
from webslicer_create_group import WebSlicer_CreateGroup


class TestWebSlicerCreateGroupBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = WebSlicer_CreateGroup
        self.e = self.effect()
