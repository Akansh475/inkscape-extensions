# coding=utf-8
from hpgl_output import HpglOutput
from tests.base import InkscapeExtensionTestMixin, TestCase


class HPGLOutputBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = HpglOutput
        self.e = self.effect()
