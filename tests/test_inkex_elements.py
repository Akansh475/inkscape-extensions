#!/usr/bin/env python
"""
Test elements extra logic from svg xml lxml custom classes.
"""
from inkex.transforms import Transform

from tests.base import TestCase
import unittest
from tests.base.svg import svg_file

class ElementTestCase(TestCase):
    """Base element test case"""
    tag = 'svg'

    def setUp(self):
        self.svg = svg_file(self.data_file('svg', 'complextransform.test.svg'))
        self.elem = self.svg.getElement('//svg:{}'.format(self.tag))

    def test_print(self):
        """Print element as string"""
        self.assertEqual(str(self.elem), self.tag)

class CoreElementTestCase(ElementTestCase):
    """Test core element functionality"""
    tag = 'g'
    def test_sort_ids(self):
        """Are the element ids sorted"""
        self.assertEqual(tuple(self.elem.sort_ids([])), ())
        self.assertEqual(tuple(self.elem.sort_ids(['A', 'B', 'C', 'D', 'E', 'F', 'G'])),
                                                  ('A', 'B', 'C', 'D', 'E', 'F', 'G'))
        self.assertEqual(tuple(self.elem.sort_ids(['G', 'B', 'D', 'F'])), ('B', 'D', 'F', 'G'))
        self.assertEqual(tuple(self.elem.sort_ids(['X', 'Y', 'Z', 'A'])), ('A',))

    def test_sort_selected(self):
        """Are the selected items sorted"""
        self.svg.set_selected('G', 'B', 'D', 'F')
        self.assertEqual(tuple(self.svg.selected), ('G', 'B', 'D', 'F'))
        items = self.svg.get_z_selected()
        self.assertTrue(isinstance(items, dict))
        self.assertEqual(tuple(items), ('B', 'D', 'F', 'G'))


class GroupTest(ElementTestCase):
    """Test extra functionality on a group element"""
    tag = 'g'

    def test_transform_property(self):
        """Test getting and setting a transform"""
        self.assertEqual(str(self.elem.transform), 'matrix(1.44985 0 0 1.36417 -107.03 -167.362)')
        self.elem.transform = 'translate(12, 14)'
        self.assertEqual(self.elem.transform, Transform('translate(12, 14)'))
        self.assertEqual(str(self.elem.transform), 'matrix(1 0 0 1 12 14)')


class RectTest(ElementTestCase):
    """Test extra functionality on a rectangle element"""
    tag = 'rect'

    def test_compose_transform(self):
        """Composed transformation"""
        self.assertEqual(self.elem.transform, Transform('rotate(16.097889)'))
        self.assertEqual(str(self.elem.composed_transform()), \
            'matrix(0.754465 -0.863362 1.13818 1.31905 -461.593 215.193)')

    def test_compose_stylesheet(self):
        """Test finding the composed stylesheet for the shape"""
        self.assertEqual(str(self.elem.style), 'fill:#0000ff;stroke-width:1px')
        self.assertEqual(str(self.elem.composed_style()), \
            'fill:#0000ff;stroke:#d88;stroke-width:1px')

    def test_path(self):
        """Rectangle path"""
        self.assertEqual(str(self.elem.path), 'M 200.0,200.0 h100.0v100.0h-100.0')


class CirtcleTest(ElementTestCase):
    """Test extra functionality on a circle element"""
    tag = 'circle'

    def test_path(self):
        """Circle path"""
        self.assertEqual(str(self.elem.path),\
            'M 50.0 150.0 A 50.0,50.0 0 1 0 150.0, 100.0 A 50.0,50.0 0 1 0 50.0, 100.0')

class UseTest(ElementTestCase):
    """Test extra functionality on a use element"""
    tag = 'use'

    def test_path(self):
        """Use path follows ref"""
        self.assertEqual(str(self.elem.path), 'M 0 0 L 10 10 Z')

if __name__ == '__main__':
    unittest.main()
