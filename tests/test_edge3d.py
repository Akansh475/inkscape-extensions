#!/usr/bin/env python

import unittest

from edge3d import Edge3d
from tests.base import InkscapeExtensionTestMixin, TestCase
import inkex

class Edge3dBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Edge3d
        self.e = self.effect()

    def test_basic(self):
        args = [
            '--id=edgeme'
            , self.data_file('svg', 'edge3d.svg')]
        e = Edge3d()
        e.run(args)
        old_paths = e.original_document.xpath('//svg:path[@id="edgeme"]', namespaces=inkex.NSS)
        new_paths = e.document.xpath('//svg:path[@id="edgeme"]', namespaces=inkex.NSS)
        self.assertTrue (len (old_paths) == 1)
        self.assertTrue (len (new_paths) == 1)
        old_paths = e.original_document.xpath('//svg:path', namespaces=inkex.NSS)
        new_paths = e.document.xpath('//svg:path', namespaces=inkex.NSS)
        self.assertTrue (len (old_paths) == 1)
        self.assertTrue (len (new_paths) == 4)

if __name__ == '__main__':
    unittest.main()
