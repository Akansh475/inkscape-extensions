# coding=utf-8
from color_darker import C
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase

class ColorDarkerBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = C

    def test_default_values_black(self):
        args = [self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_white(self):
        args = [self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(255, 255, 255)
        self.assertEqual("e6e6e6", col)

    def test_default_values_silver(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Silver
        col = self.effect.colmod(192, 192, 192)
        self.assertEqual("adadad", col)

    def test_default_values_grey(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Grey
        col = self.effect.colmod(128, 128, 128)
        self.assertEqual("737373", col)

    def test_default_values_maroon(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Maroon
        col = self.effect.colmod(128, 0, 0)
        self.assertEqual("730000", col)

    def test_default_values_red(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Red
        col = self.effect.colmod(255, 0, 0)
        self.assertEqual("e60000", col)

    def test_default_values_olive(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Olive
        col = self.effect.colmod(128, 128, 0)
        self.assertEqual("737300", col)

    def test_default_values_yellow(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Yellow
        col = self.effect.colmod(255, 255, 0)
        self.assertEqual("e6e600", col)

    def test_default_values_green(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Green
        col = self.effect.colmod(0, 128, 0)
        self.assertEqual("007300", col)

    def test_default_values_lime(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Lime
        col = self.effect.colmod(0, 255, 0)
        self.assertEqual("00e600", col)

    def test_default_values_teal(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Teal
        col = self.effect.colmod(0, 128, 128)
        self.assertEqual("007373", col)

    def test_default_values_aqua(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Aqua
        col = self.effect.colmod(0, 255, 255)
        self.assertEqual("00e6e6", col)

    def test_default_values_navy(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Navy
        col = self.effect.colmod(0, 0, 128)
        self.assertEqual("000073", col)

    def test_default_values_blue(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Blue
        col = self.effect.colmod(0, 0, 255)
        self.assertEqual("0000e6", col)

    def test_default_values_purple(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Purple
        col = self.effect.colmod(128, 0, 128)
        self.assertEqual("730073", col)

    def test_default_values_fuschia(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Fuschia
        col = self.effect.colmod(255, 0, 255)
        self.assertEqual("e600e6", col)
