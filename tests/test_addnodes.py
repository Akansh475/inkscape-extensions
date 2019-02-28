#!/usr/bin/en
# coding=utf-8

import unittest

from addnodes import SplitIt
from tests.base import InkscapeExtensionTestMixin, TestCase


class SplitItBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SplitIt
        self.e = self.effect()


    def test_basic(self):
        args = [
            '--id=dashme'
            , self.data_file('svg', 'dash.svg')]
        e = SplitIt()
        e.run(args)
        old_path = e.original_document.xpath('//svg:path', namespaces=inkex.NSS)[0].path
        new_path = e.document.xpath('//svg:path', namespaces=inkex.NSS)[0].path
        self.assertTrue (len(new_path) > len (old_path))

if __name__ == '__main__':
    unittest.main()
