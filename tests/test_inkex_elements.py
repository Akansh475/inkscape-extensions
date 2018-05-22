#!/usr/bin/env python
"""
Test elements extra logic from svg xml lxml custom classes.
"""
from inkex.transforms import Transform

from tests.base import TestCase, test_support
from tests.base.svg import svg_file


class GroupTest(TestCase):
    """Test extra functionality on a group element"""
    def setUp(self):
        self.svg = svg_file(self.data_file('svg', 'complextransform.test.svg'))
        self.group = self.svg.getElement("//svg:g")
        self.rect = self.svg.getElement("//svg:rect")

    def test_transform_property(self):
        """Test getting and setting a transform"""
        self.assertEqual(str(self.group.transform), 'matrix(1.44985 0 0 1.36417 -107.03 -167.362)')
        self.group.transform = 'translate(12, 14)'
        self.assertEqual(self.group.transform, Transform('translate(12, 14)'))
        self.assertEqual(str(self.group.transform), 'matrix(1 0 0 1 12 14)')

    def test_compose_transform(self):
        """Test loading a group, group, and compose the transformation"""
        self.assertEqual(self.rect.transform, Transform('rotate(16.097889)'))
        self.assertEqual(str(self.rect.composed_transform()), \
            'matrix(0.754465 -0.863362 1.13818 1.31905 -461.593 215.193)')

    def test_compose_stylesheet(self):
        """Test finding the composed stylesheet for the shape"""
        self.assertEqual(str(self.rect.style), 'fill:#0000ff;stroke-width:1px')
        self.assertEqual(str(self.rect.composed_style()), \
            'fill:#0000ff;stroke:#d88;stroke-width:1px')



if __name__ == '__main__':
    test_support.run_unittest(GroupTest)
