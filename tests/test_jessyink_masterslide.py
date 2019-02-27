#!/usr/bin/en
# coding=utf-8

import unittest

from jessyInk_masterSlide import JessyInk_MasterSlide
from tests.base import InkscapeExtensionTestMixin, TestCase


class JessyInkMasterSlideBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JessyInk_MasterSlide
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
