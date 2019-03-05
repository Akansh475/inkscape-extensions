# coding=utf-8
from straightseg import SegmentStraightener
from tests.base import InkscapeExtensionTestMixin, TestCase


class SegmentStraightenerBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = SegmentStraightener
        self.e = self.effect()
