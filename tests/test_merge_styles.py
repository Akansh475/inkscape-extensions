# coding=utf-8
from merge_styles import MergeStyles
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestMergeStylesBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = MergeStyles
        self.e = self.effect()
