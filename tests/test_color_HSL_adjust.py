# coding=utf-8
from color_HSL_adjust import C
from inkex.tester import ComparisonMixin, InkscapeExtensionTestMixin, TestCase


class ColorHSLAdjustBasicTest(ComparisonMixin, InkscapeExtensionTestMixin, TestCase):
    effect_class = C

    def test_default_values(self):
        """ The default ranges are set to 0, and thus the color should not change. """
        args = [self.empty_svg]
        self.effect.run(args)
        col = self.effect.colmod(255, 255, 255)
        self.assertEqual("ffffff", col)

        col = self.effect.colmod(0, 0, 0)
        self.assertEqual("000000", col)

        col = self.effect.colmod(0, 128, 0)
        self.assertEqual("008000", col)

    def test_small_hue_value(self):
        args = ['-x 10', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5b97b0", col)

    def test_large_hue_value(self):
        args = ['-x 320', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5bb081", col)

    def test_nil_hue_value(self):
        args = ['-x 0', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5ba5b0", col)

    def test_largest_hue_value(self):
        args = ['-x 360', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5ba6b0", col)

    def test_too_large_hue_value(self):
        args = ['-x 12345', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("a45bb0", col)

    def test_negative_hue_value(self):
        args = ['-x -1', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5ba7b0", col)

    def test_small_saturation_value(self):
        args = ['-s 10', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("4eafbc", col)

    def test_large_saturation_value(self):
        args = ['-s 90', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("0ce2fe", col)

    def test_nil_saturation_value(self):
        args = ['-s 0', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5ba5b0", col)

    def test_largest_saturation_value(self):
        args = ['-s 100', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("0ce2fe", col)

    def test_too_large_saturation_value(self):
        args = ['-s 12345', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("0ce2fe", col)

    def test_negative_saturation_value(self):
        args = ['-s -1', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5ca5ae", col)

    def test_small_lightness_value(self):
        args = ['-l 10', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("7db8c0", col)

    def test_large_lightness_value(self):
        args = ['-l 90', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("ffffff", col)

    def test_nil_lightness_value(self):
        args = ['-l 0', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("5ba5b0", col)

    def test_largest_lightness_value(self):
        args = ['-l 100', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("ffffff", col)

    def test_too_large_lightness_value(self):
        args = ['-l 12345', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("ffffff", col)

    def test_negative_lightness_value(self):
        args = ['-l -1', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertEqual("57a4ae", col)

    def test_random_hue_value(self):
        args = ['--random_h=true', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertNotEqual("5ba6b0", col)

    def test_random_lightness_value(self):
        args = ['--random_l=true', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertNotEqual("5ba6b0", col)

    def test_random_saturation_value(self):
        args = ['--random_s=true', self.empty_svg]
        self.effect.run(args)
        # 5ba6b0
        col = self.effect.colmod(91, 166, 176)
        self.assertNotEqual("5ba6b0", col)
