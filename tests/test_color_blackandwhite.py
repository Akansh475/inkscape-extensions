# coding=utf-8
from color_blackandwhite import C
from tests.base import InkscapeExtensionTestMixin, TestCase


class ColorBlackAndWhiteBasicTest(InkscapeExtensionTestMixin, TestCase):
    def setUp(self):
        self.effect = C
        self.e = self.effect()

    def test_default_values_black(self):
        """
        When converting to black and white the color black should be unchanged
        """
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_white(self):
        """
        When converting to black and white the color white should be unchanged
        """
        args = [self.empty_svg]
        self.e.run(args)
        col = self.e.colmod(255, 255, 255)
        self.assertEqual("ffffff", col)

    def test_default_values_silver(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Silver
        col = self.e.colmod(192, 192, 192)
        self.assertEqual("ffffff", col)

    def test_default_values_grey(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Grey
        col = self.e.colmod(128, 128, 128)
        self.assertEqual("ffffff", col)

    def test_default_values_maroon(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Maroon
        col = self.e.colmod(128, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_red(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Red
        col = self.e.colmod(255, 0, 0)
        self.assertEqual("000000", col)

    def test_default_values_olive(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Olive
        col = self.e.colmod(128, 128, 0)
        self.assertEqual("000000", col)

    def test_default_values_yellow(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Yellow
        col = self.e.colmod(255, 255, 0)
        self.assertEqual("ffffff", col)

    def test_default_values_green(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Green
        col = self.e.colmod(0, 128, 0)
        self.assertEqual("000000", col)

    def test_default_values_lime(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Lime
        col = self.e.colmod(0, 255, 0)
        self.assertEqual("ffffff", col)

    def test_default_values_teal(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Teal
        col = self.e.colmod(0, 128, 128)
        self.assertEqual("000000", col)

    def test_default_values_aqua(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Aqua
        col = self.e.colmod(0, 255, 255)
        self.assertEqual("ffffff", col)

    def test_default_values_navy(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Navy
        col = self.e.colmod(0, 0, 128)
        self.assertEqual("000000", col)

    def test_default_values_blue(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Blue
        col = self.e.colmod(0, 0, 255)
        self.assertEqual("000000", col)

    def test_default_values_purple(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Purple
        col = self.e.colmod(128, 0, 128)
        self.assertEqual("000000", col)

    def test_default_values_fuschia(self):
        args = [self.empty_svg]
        self.e.run(args)

        # Fuschia
        col = self.e.colmod(255, 0, 255)
        self.assertEqual("000000", col)

    def test_large_threshold(self):
        """
        Increasing the threshold means more colors will be black
        """

        args = ['-t 240', self.empty_svg]
        self.e.run(args)

        # Fuschia
        col = self.e.colmod(255, 0, 255)
        self.assertEqual("000000", col)

        # Silver
        col = self.e.colmod(192, 192, 192)
        self.assertEqual("000000", col)

    def test_small_threshold(self):
        """
        Decreasing the threshold means more colors will be white
        """

        args = ['-t 80', self.empty_svg]
        self.e.run(args)

        # Fuschia
        col = self.e.colmod(255, 0, 255)
        self.assertEqual("ffffff", col)

        # Silver
        col = self.e.colmod(192, 192, 192)
        self.assertEqual("ffffff", col)
