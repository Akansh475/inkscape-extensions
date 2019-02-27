#!/usr/bin/env python
# coding=utf-8

import unittest

from tar_layers import LayersOutput
from tests.base import InkscapeExtensionTestMixin, TestCase


class LayersOutputBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = LayersOutput
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
