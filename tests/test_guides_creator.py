#!/usr/bin/env python
# coding=utf-8
from guides_creator import GuidesCreator
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class GuidesCreatorBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = GuidesCreator
