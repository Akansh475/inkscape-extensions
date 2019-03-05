# coding=utf-8
from render_gear_rack import RackGear
from tests.base import InkscapeExtensionTestMixin, TestCase


class TestRackGearBasic(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = RackGear
        self.e = self.effect()
