#!/usr/bin/env python
# coding=utf-8
"""
Test all selection code.
"""

from .test_inkex_elements_base import SvgTestCase

class ElementSelectionsTestCase(SvgTestCase):
    """Test Element Selections"""
    def test_sort_selected(self):
        """Are the selected items sorted"""
        self.svg.selection.set('G', 'B', 'D', 'F')
        self.assertEqual(tuple(self.svg.selection.ids()), ('G', 'B', 'D', 'F'))
        items = self.svg.selection.paint_order()
        self.assertTrue(isinstance(items, dict))
        self.assertEqual(tuple(items.ids()), ('B', 'D', 'F', 'G'))
        self.svg.selected.set()
        self.assertEqual(tuple(self.svg.selection), ())
        a_to_g = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        self.svg.selection.set(*a_to_g)
        self.assertEqual(tuple(self.svg.selection.paint_order().ids()), a_to_g)
        self.svg.selected.set('X', 'Y', 'Z', 'A')
        self.assertEqual(tuple(self.svg.selection.paint_order().ids()), ('A',))
