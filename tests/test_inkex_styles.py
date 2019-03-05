# coding=utf-8
"""
Test Inkex style parsing functionality.
"""
from inkex.styles import Style
from tests.base import TestCase


class StyleTest(TestCase):
    """Test path API and calculations"""

    def test_new_style(self):
        """Create a style from a path string"""
        stl = Style("border-color: blue; border-width: 4px;")
        self.assertEqual(str(stl), 'border-color:blue;border-width:4px')

    def test_composite(self):
        """Test chaining styles together"""
        stl = Style("border-color: blue;")
        stl += "border-color: red; border-issues: true;"
        self.assertEqual(str(stl), 'border-color:red;border-issues:true')
        st2 = stl + "border-issues: false;"
        self.assertEqual(str(st2), 'border-color:red;border-issues:false')

    def test_set_property(self):
        """Set the style attribute directly"""
        stl = Style()
        stl['border-pain'] = 'green'
        self.assertEqual(str(stl), 'border-pain:green')
