# coding=utf-8
from render_gears import Gears
from tests.base import InkscapeExtensionTestMixin, TestCase


class GearsBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = Gears
        self.e = self.effect()
