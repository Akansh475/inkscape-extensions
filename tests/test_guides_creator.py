#!/usr/bin/env python
# coding=utf-8

import unittest

from guides_creator import GuidesCreator
from tests.base import InkscapeExtensionTestMixin, TestCase


class GuidesCreatorBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = GuidesCreator
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
