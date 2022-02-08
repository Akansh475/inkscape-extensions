#!/usr/bin/env python
# coding=utf-8
from guides_creator import GuidesCreator
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareNumericFuzzy


class GuidesCreatorBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    """Basic tests for GuidesCreator"""

    effect_class = GuidesCreator
    compare_file = "svg/guides.svg"
    compare_filters = [
        CompareNumericFuzzy(),
    ]
    old_defaults = (
        "--vertical_guides=3",
        "--ul=True",
        "--ur=True",
        "--ll=True",
        "--lr=True",
        "--header_margin=6",
        "--footer_margin=6",
        "--left_margin=6",
        "--right_margin=6",
    )
    comparisons = [
        old_defaults + ("--tab=regular_guides", "--guides_preset=custom"),
        old_defaults
        + ("--tab=regular_guides", "--guides_preset=golden", "--delete=True"),
        old_defaults
        + ("--tab=regular_guides", "--guides_preset=5;5", "--start_from_edges=True"),
        old_defaults + ("--tab=diagonal_guides", "--nodup=False"),
        old_defaults
        + ("--tab=margins", "--start_from_edges=True", "--margins_preset=custom"),
        old_defaults
        + ("--tab=margins", "--start_from_edges=True", "--margins_preset=book_left"),
        old_defaults
        + ("--tab=margins", "--start_from_edges=True", "--margins_preset=book_right"),
    ]


class GuidesCreatorMillimeterTest(ComparisonMixin, TestCase):
    """Test that guides are correctly created in a mm based document"""

    effect_class = GuidesCreator
    compare_file = "svg/complextransform.test.svg"
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [
        ("--vertical_guides=6", "--horizontal_guides=8"),
        ("--tab=regular_guides", "--start_from_edges=True", "--guides_preset=golden"),
        (
            "--tab=regular_guides",
            "--start_from_edges=True",
            "--guides_preset=custom",
            "--vertical_guides=4",
            "--horizontal_guides=5",
        ),
        (
            "--tab=margins",
            "--start_from_edges=False",
            "--margins_preset=book_right",
            "--vert=3",
            "--horz=2",
        ),
    ]


class GuidesCreatorFunctionalityTests(TestCase):
    """Test some methods on their own"""

    def test_page_descriptor(self):
        """Test that page descriptions are parsed correctly"""

        def parsetest(string, length, comparison):
            self.assertTupleEqual(
                GuidesCreator.parse_page_descriptor(string, length), comparison
            )

        parsetest("1, 2,3", 10, (1, 2, 3))
        parsetest("1-3, 5, 10", 10, (1, 2, 3, 5, 10))
        parsetest("2, 4-, 6, 7-", 10, (2, 4, 5, 6, 7, 8, 9, 10))
        parsetest("2-5, 7-9, 10-", 12, (2, 3, 4, 5, 7, 8, 9, 10, 11, 12))
        parsetest("6, 7, 8", 3, tuple())
        parsetest("2, 216-218, 10", 300, (2, 10, 216, 217, 218))


class GuidesTestMulitpage(ComparisonMixin, TestCase):
    """Test multipage functionality"""

    effect_class = GuidesCreator
    compare_file = "svg/empty_multipage.svg"
    compare_filters = [CompareNumericFuzzy()]
    comparisons = [
        (),  # by default, all pages
        # selection of pages
        ("--vertical_guides=4", "--horizontal_guides=3", "--pages=1,,3-7,12"),
        # diagonal guides
        (
            "--tab=diagonal_guides",
            "--nodup=False",
            "--pages=1-3",
            "--ul=True",
            "--ur=True",
            "--ll=True",
            "--lr=True",
        ),
        # There is one diagonal guide already in the file, it should be unchanged
        (
            "--tab=diagonal_guides",
            "--nodup=True",
            "--pages=1-3",
            "--ul=True",
            "--ur=True",
            "--ll=True",
            "--lr=True",
        ),
        (
            "--tab=margins",
            "--start_from_edges=True",
            "--margins_preset=book_alternating_left",
        ),
        (
            "--tab=margins",
            "--start_from_edges=False",
            "--margins_preset=book_alternating_right",
        ),
    ]
