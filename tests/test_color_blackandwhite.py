# coding=utf-8
from color_blackandwhite import C
from tests.base import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class ColorBlackAndWhiteBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = C

    def test_default_values_black(self):
        """
        When converting to black and white the color black should be unchanged
        """
        args = [self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_white(self):
        """
        When converting to black and white the color white should be unchanged
        """
        args = [self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(255, 255, 255)
        self.assertEqual("ffffff", col)

    def test_default_values_silver(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Silver
        col = self.effect.colmod(192, 192, 192)
        self.assertEqual("ffffff", col)

    def test_default_values_grey(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Grey
        col = self.effect.colmod(128, 128, 128)
        self.assertEqual("ffffff", col)

    def test_default_values_maroon(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Maroon
        col = self.effect.colmod(128, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_red(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Red
        col = self.effect.colmod(255, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_olive(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Olive
        col = self.effect.colmod(128, 128, 0)
        self.assertEqual("000000", col)

    def test_default_values_yellow(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Yellow
        col = self.effect.colmod(255, 255, 0)
        self.assertEqual("ffffff", col)

    def test_default_values_green(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Green
        col = self.effect.colmod(0, 128, 0)
        self.assertEqual("000000", col)

    def test_default_values_lime(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Lime
        col = self.effect.colmod(0, 255, 0)
        self.assertEqual("ffffff", col)

    def test_default_values_teal(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Teal
        col = self.effect.colmod(0, 128, 128)
        self.assertEqual("000000", col)

    def test_default_values_aqua(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Aqua
        col = self.effect.colmod(0, 255, 255)
        self.assertEqual("ffffff", col)

    def test_default_values_navy(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Navy
        col = self.effect.colmod(0, 0, 128)
        self.assertEqual("000000", col)

    def test_default_values_blue(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Blue
        col = self.effect.colmod(0, 0, 255)
        self.assertEqual("000000", col)

    def test_default_values_purple(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Purple
        col = self.effect.colmod(128, 0, 128)
        self.assertEqual("000000", col)

    def test_default_values_fuschia(self):
        args = [self.empty_svg]
        self.effect.run(args)

        # Fuschia
        col = self.effect.colmod(255, 0, 255)
        self.assertEqual("000000", col)

    def test_large_threshold(self):
        """
        Increasing the threshold means more colors will be black
        """

        args = ['-t 240', self.empty_svg]
        self.effect.run(args)

        # Fuschia
        col = self.effect.colmod(255, 0, 255)
        self.assertEqual("000000", col)

        # Silver
        col = self.effect.colmod(192, 192, 192)
        self.assertEqual("000000", col)

    def test_small_threshold(self):
        """
        Decreasing the threshold means more colors will be white
        """

        args = ['-t 80', self.empty_svg]
        self.effect.run(args)

        # Fuschia
        col = self.effect.colmod(255, 0, 255)
        self.assertEqual("ffffff", col)

        # Silver
        col = self.effect.colmod(192, 192, 192)
        self.assertEqual("ffffff", col)
