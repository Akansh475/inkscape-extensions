#!/usr/bin/en
# coding=utf-8

import unittest

from addnodes import SplitIt
from inkex import NSS
from tests.base import InkscapeExtensionTestMixin, TestCase


class SplitItBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SplitIt
        self.e = self.effect()

    def test_basic(self):
        args = ['--id=dashme',
                self.data_file('svg', 'dash.svg')]
        self.e.run(args)
        old_path = self.e.original_document.xpath('//svg:path', namespaces=NSS)[0].path
        new_path = self.e.document.xpath('//svg:path', namespaces=NSS)[0].path
        assert len(new_path) > len(old_path)


if __name__ == '__main__':
    unittest.main()
