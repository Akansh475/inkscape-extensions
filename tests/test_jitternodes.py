# coding=utf-8
from jitternodes import JitterNodes
from inkex.tester import InkscapeExtensionTestMixin, TestCase


class JitterNodesBasicTest(InkscapeExtensionTestMixin, TestCase):
    effect_class = JitterNodes
