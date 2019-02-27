#!/usr/bin/env python
# coding=utf-8

import unittest

from measure import Length
from tests.base import InkscapeExtensionTestMixin, TestCase


class LengthBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Length
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
