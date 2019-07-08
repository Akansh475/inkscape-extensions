#!/usr/bin/env python
# coding=utf-8
from guides_creator import GuidesCreator
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class GuidesCreatorBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = GuidesCreator
    compare_filters = [CompareNumericFuzzy(),]

    comparisons = [
        ('--tab=regular_guides', '--guides_preset=custom'),
        ('--tab=regular_guides', '--guides_preset=golden'),
        ('--tab=regular_guides', '--guides_preset=5;5'),
        ('--tab=diagonal_guides',),
        ('--tab=margins', '--start_from_edges2=True', '--margins_preset=custom'),
        ('--tab=margins', '--start_from_edges2=True', '--margins_preset=book_left'),
        ('--tab=margins', '--start_from_edges2=True', '--margins_preset=book_right'),
    ]
