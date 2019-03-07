# coding=utf-8
from color_grayscale import C
from tests.base import InkscapeExtensionTestMixin, TestCase


class ColorGrayscaleBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()

    def test_default_values_black(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_white(self):
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(255, 255, 255)
        self.assertEqual("ffffff", col)

    def test_default_values_silver(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Silver
        col = self.e.colmod(192, 192, 192)
        self.assertEqual("c0c0c0", col)

    def test_default_values_grey(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Grey
        col = self.e.colmod(128, 128, 128)
        self.assertEqual("808080", col)

    def test_default_values_maroon(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Maroon
        col = self.e.colmod(128, 0, 0)
        self.assertEqual("262626", col)

    def test_default_values_red(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Red
        col = self.e.colmod(255, 0, 0)
        self.assertEqual("4c4c4c", col)

    def test_default_values_olive(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Olive
        col = self.e.colmod(128, 128, 0)
        self.assertEqual("717171", col)

    def test_default_values_yellow(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Yellow
        col = self.e.colmod(255, 255, 0)
        self.assertEqual("e2e2e2", col)

    def test_default_values_green(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Green
        col = self.e.colmod(0, 128, 0)
        self.assertEqual("4b4b4b", col)

    def test_default_values_lime(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Lime
        col = self.e.colmod(0, 255, 0)
        self.assertEqual("969696", col)

    def test_default_values_teal(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Teal
        col = self.e.colmod(0, 128, 128)
        self.assertEqual("5a5a5a", col)

    def test_default_values_aqua(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Aqua
        col = self.e.colmod(0, 255, 255)
        self.assertEqual("b3b3b3", col)

    def test_default_values_navy(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Navy
        col = self.e.colmod(0, 0, 128)
        self.assertEqual("0f0f0f", col)

    def test_default_values_blue(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Blue
        col = self.e.colmod(0, 0, 255)
        self.assertEqual("1d1d1d", col)

    def test_default_values_purple(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Purple
        col = self.e.colmod(128, 0, 128)
        self.assertEqual("353535", col)

    def test_default_values_fuschia(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Fuschia
        col = self.e.colmod(255, 0, 255)
        self.assertEqual("696969", col)
