#!/usr/bin/env python

import unittest

from embedimage import Embedder
from tests.base import InkscapeExtensionTestMixin, TestCase


class EmbedderBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Embedder
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
