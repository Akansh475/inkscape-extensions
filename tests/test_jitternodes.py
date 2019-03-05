# coding=utf-8
from jitternodes import JitterNodes
from tests.base import InkscapeExtensionTestMixin, TestCase


class JitterNodesBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = JitterNodes
        self.e = self.effect()
