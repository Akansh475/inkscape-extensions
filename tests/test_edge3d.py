#!/usr/bin/env python
# coding=utf-8
import inkex
from edge3d import Edge3d
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareNumericFuzzy, CompareWithPathSpace


class Edge3dBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = Edge3d
    compare_filters = [CompareNumericFuzzy(), CompareWithPathSpace()]

    def test_basic(self):
        args = ['--id=edgeme',
                self.data_file('svg', 'edge3d.svg')]
        self.effect.run(args)
        old_paths = self.effect.original_document\
            .xpath('//svg:path[@id="edgeme"]', namespaces=inkex.NSS)
        new_paths = self.effect.document.xpath('//svg:path[@id="edgeme"]', namespaces=inkex.NSS)
        self.assertTrue(len(old_paths) == 1)
        self.assertTrue(len(new_paths) == 1)
        old_paths = self.effect.original_document.xpath('//svg:path', namespaces=inkex.NSS)
        new_paths = self.effect.document.xpath('//svg:path', namespaces=inkex.NSS)
        self.assertTrue(len(old_paths) == 1)
        self.assertTrue(len(new_paths) == 4)
