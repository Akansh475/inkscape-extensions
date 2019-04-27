# coding=utf-8

from color_custom import C
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class ColorCustomBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = C
    comparisons = [
        ('--scale=100', '--r=100', '--g=50', '--b=0'),
    ]

    def test_default_values(self):
        """ The default ranges are set to 0, and thus the color should not change. """
        args = [self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(255, 255, 255)
        self.assertEqual("ffffff", col)

    def test_double_red(self):
        args = ['-r r*2', self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(100, 0, 0)
        self.assertEqual("c80000", col)

    def test_switch_green_blue(self):
        args = ['-g b', '-b g', self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(12, 34, 56)
        self.assertEqual("0c3822", col)

    def test_switch_green_blue_and_double_red(self):
        args = ['-g b', '-b g', '-r r*2', self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(12, 34, 56)
        self.assertEqual("183822", col)

    def test_set_red_to_16_scale255(self):
        args = ['-s 255', '-r 16', self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(0, 0, 0)
        self.assertEqual("100000", col)

    def test_set_red_to_16_scale1(self):
        args = ['-s 1', '-r 0.0625', self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(0, 0, 0)
        self.assertEqual("100000", col)

    def test_set_red_to_400(self):
        """This should cap red at 255"""
        args = ['-r 400', self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(0, 0, 0)
        self.assertEqual("ff0000", col)

    def test_set_red_to_negative(self):
        """This should cap red at 0"""
        args = ['-r -400', self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(0, 0, 0)
        self.assertEqual("000000", col)

    def test_evil_fails(self):
        """
        eval shouldn't allow for evil things to happen

        Here we try and check if a file exists but it could just as easily
        overwrite or delete the file

        """

        args = ["-r __import__('os').path.exists('__init__.py')", self.empty_svg]
        self.effect.run(args)

        with self.assertRaises(TypeError):
            self.effect.colmod(0, 0, 0)

    def test_invalid_operator(self):
        args = ["-r r % 100", self.empty_svg]
        self.effect.run(args)

        with self.assertRaises(KeyError):
            self.effect.colmod(0, 0, 0)

    def test_bad_syntax(self):
        args = ["-r r + 100)", self.empty_svg]
        self.effect.run(args)

        with self.assertRaises(SyntaxError):
            self.effect.colmod(0, 0, 0)
