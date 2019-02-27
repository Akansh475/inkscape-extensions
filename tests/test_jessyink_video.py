#!/usr/bin/en
# coding=utf-8

import unittest

from jessyInk_video import JessyInk_Effects
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkEffectsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_Effects
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
