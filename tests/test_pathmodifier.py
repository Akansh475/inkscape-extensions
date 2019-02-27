#!/usr/bin/env python
# coding=utf-8

import unittest

from pathmodifier import PathModifier
from tests.base import InkscapeExtensionTestMixin, TestCase


class PathModifierBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = PathModifier
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
