# coding=utf-8
from inkscape_follow_link import FollowLink
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestFollowLinkBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = FollowLink
        self.e = self.effect()
