#!/usr/bin/env python
# coding=utf-8

import unittest

from handles import Handles
from tests.base import InkscapeExtensionTestMixin, TestCase


class HandlesBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Handles
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
