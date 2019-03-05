# coding=utf-8
from foldablebox import FoldableBox
from tests.base import InkscapeExtensionTestMixin, TestCase


class FoldableBoxArguments(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = FoldableBox
        self.e = self.effect()

    def test_basic_box_elements(self):
        e = FoldableBox()
        e.affect([self.empty_svg])
        self.assertEqual(e.box.tag, 'g', 'The box group must be created.')
        self.assertEqual(len(e.box.getchildren()), 13, 'The box group must have 13 childs.')
