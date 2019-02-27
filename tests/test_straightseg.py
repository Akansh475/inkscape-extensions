#!/usr/bin/env python
# coding=utf-8

import unittest

from straightseg import SegmentStraightener
from tests.base import InkscapeExtensionTestMixin, TestCase


class SegmentStraightenerBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SegmentStraightener
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
