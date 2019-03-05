# coding=utf-8
from color_replace import C
from tests.base import InkscapeExtensionTestMixin, TestCase


class ColorRemoveBlueBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()

    def test_default_values_match(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_no_match(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(128, 0, 0)
        self.assertEqual("800000", col)

    def test_default_from_different_to(self):
        args = ["-t696969", self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(0, 0, 0)
        self.assertEqual("696969", col)

    def test_from_color_doesnt_match(self):
        args = ["-f123456", "-t696969", self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_from_color_does_match(self):
        args = ["-f123456", "-t696969", self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(18, 52, 86)
        self.assertEqual("696969", col)

    def test_from_color_no_to_color(self):
        args = ["-f123456", self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(18, 52, 86)
        self.assertEqual("000000", col)
