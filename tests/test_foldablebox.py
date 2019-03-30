# coding=utf-8
from foldablebox import FoldableBox
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase
from tests.base.filters import CompareOrderIndependentStyle

class FoldableBoxArguments(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect = FoldableBox
    compare_filters = [CompareOrderIndependentStyle()]

    def test_basic_box_elements(self):
        self.e.run([self.empty_svg])
        self.assertEqual(self.e.box.tag, 'g', 'The box group must be created.')
        self.assertEqual(len(self.e.box.getchildren()), 13, 'The box group must have 13 childs.')
