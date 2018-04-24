#!/usr/bin/env python
"""
Test elements extra logic from svg xml lxml custom classes.
"""

from tests.base import TestCase, test_support

from inkex.elements import Group

class GroupTest(TestCase):
    """Test extra functionality on a group element"""
    def test_compose_transform(self):
        """Test loading a group, group, and compose the transformation"""
        raise NotImplementedError("Write this test")

    def test_transform_property(self):
        """Test getting and setting a transform"""
        matrix = group.transform
        self.assertEqual(matrix, None)
        group.transform = 'translate(12, 14)'
        matrix = group.transform
        self.assertEqual(matrix, Transform)
        self.assertEqual(str(matrix), 'FILL ME')
        self.assertEqual(str(group), '<g FILL ME>')



if __name__ == '__main__':
    test_support.run_unittest(GroupTest)
