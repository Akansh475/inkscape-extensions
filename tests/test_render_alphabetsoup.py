#!/usr/bin/env python
# coding=utf-8

import unittest

from render_alphabetsoup import AlphabetSoup
from tests.base import InkscapeExtensionTestMixin, TestCase


class AlphabetSoupBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = AlphabetSoup
        self.e = self.effect()


if __name__ == '__main__':
    unittest.main()
