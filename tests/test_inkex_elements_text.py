#!/usr/bin/env python3
# coding=utf-8
"""
Test the element API text classes and basic functionality
"""

from inkex.elements import (
    TextElement,
)

from inkex.tester import TestCase
from inkex.tester.svg import svg_file


class SvgTestCase(TestCase):
    """Test SVG"""

    source_file = "text_with_nested_tspan.svg"

    def setUp(self):
        super().setUp()
        self.svg = svg_file(self.data_file("svg", self.source_file))


class TextElementTestCase(SvgTestCase):
    """Test text element functions"""

    def test_get_text(self):
        """Get text should get inside its boundary, tspans included"""
        elem = self.svg.getElementById("main")

        expected_texts = [
            "Text Base",
            "tspan 1",
            "tail 1",
            "tspan 2",
            "tspan 3",
            "tspan 4",
            "tail 4",
            "Parent 1 tspan",
            "Child 1 tspan",
            "Child 2 tspan",
            "Child 2 tail",
            "Parent 1 tail",
            "Grandparent 1 tspan",
            "Parent 2 tspan",
            "Parent 3 tspan",
            "Child 3 tspan",
            "Child 4 tspan",
            "Child 4 tail",
            "Parent 3 tail",
            "Grandparent 1 tail",
            "tspan 5",
            "tspan 6",
            "tail 6",
            "Child 5 tspan",
            "Parent 4 tail",
            "The end",
        ]
        actual_texts = elem.get_text(sep="").strip().split("\n")

        # Test same number of elements
        self.assertEqual(len(expected_texts), len(actual_texts))

        # Test equality element wise
        for expected, actual in zip(expected_texts, actual_texts):
            self.assertEqual(expected, actual)
