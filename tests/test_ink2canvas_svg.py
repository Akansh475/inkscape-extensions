#!/usr/bin/en
# coding=utf-8

import unittest

from ink2canvas import Ink2Canvas
from tests.base import InkscapeExtensionTestMixin, TestCase


class Ink2CanvasBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Ink2Canvas
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
