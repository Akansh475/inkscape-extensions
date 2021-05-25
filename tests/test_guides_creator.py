#!/usr/bin/env python
# coding=utf-8
from guides_creator import GuidesCreator
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy

class GuidesCreatorBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = GuidesCreator
    compare_file = 'svg/guides.svg'
    compare_filters = [CompareNumericFuzzy(),]
    old_defaults = ('--vertical_guides=3', '--ul=True', '--ur=True', '--ll=True', '--lr=True',
                    '--header_margin=6', '--footer_margin=6', '--left_margin=6', '--right_margin=6')
    comparisons = [
        old_defaults + ('--tab=regular_guides', '--guides_preset=custom'),
        old_defaults + ('--tab=regular_guides', '--guides_preset=golden', '--delete=True'),
        old_defaults + ('--tab=regular_guides', '--guides_preset=5;5', '--start_from_edges=True'),
        old_defaults + ('--tab=diagonal_guides',),
        old_defaults + ('--tab=margins', '--start_from_edges=True', '--margins_preset=custom'),
        old_defaults + ('--tab=margins', '--start_from_edges=True', '--margins_preset=book_left'),
        old_defaults + ('--tab=margins', '--start_from_edges=True', '--margins_preset=book_right'),
    ]
