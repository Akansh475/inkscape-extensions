#!/usr/bin/env python
# coding=utf-8

import unittest

from media_zip import CompressedMediaOutput
from tests.base import InkscapeExtensionTestMixin, TestCase


class CompressedMediaOutputBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = CompressedMediaOutput
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
