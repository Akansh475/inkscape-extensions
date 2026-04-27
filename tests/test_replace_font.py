# coding=utf-8
from replace_font import ReplaceFont
from inkex.localization import inkex_gettext as _
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle
from inkex.tester.filters import WindowsTextCompat


class TestReplaceFontBasic(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = ReplaceFont
    compare_filters = [CompareOrderIndependentStyle()]
    comparisons = [
        (
            "--action=find_replace",
            "--fr_find=sans-serif",
            "--fr_replace=monospace",
        )
    ]


class TestFontList(ComparisonMixin, TestCase):
    effect_class = ReplaceFont
    comparisons = [
        ("--action=list_only",),
    ]
    stderr_output = True
    compare_filters = [WindowsTextCompat()]


class TestReplaceFontNoText(TestCase):
    effect_class = ReplaceFont
    stderr_output = True

    def testNoText(self):
        """Find and replace when there isn't any text returns error message."""

        effect = self.assertEffect(action="find_replace", fr_find="a", fr_replace="b")
        self.assertTrue(
            effect.test_output.getvalue().startswith(_("There was nothing selected"))
        )
