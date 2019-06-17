# coding=utf-8
#
# Unit test file for ../markers_strokepaint.py
# Revision history:
#  * 2012-01-27 (jazzynico): checks defaulf parameters and file handling.
#
import inkex
from markers_strokepaint import MarkerStrokePaintEffect
from inkex.tester import InkscapeExtensionTestMixin, TestCase


class MarkerStrokePaintBasicTest(InkscapeExtensionTestMixin, TestCase):
    effect_class = MarkerStrokePaintEffect

    def test_empty_defs(self):
        e = MarkerStrokePaintEffect()
        e.run([self.data_file('svg', 'minimal-blank.svg')])
        self.assertTrue(0 < len(e.svg.xpath('//svg:defs')))

    def test_basic(self):
        args = ['--id=dimension',
                self.data_file('svg', 'markers.svg')]
        e = MarkerStrokePaintEffect()
        e.run(args)
        old_markers = e.original_document.getroot().xpath('//svg:defs//svg:marker')
        new_markers = e.svg.xpath('//svg:defs//svg:marker')
        self.assertEqual(len(old_markers), 2)
        self.assertEqual(len(new_markers), 4)
