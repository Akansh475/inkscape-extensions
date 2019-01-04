#!/usr/bin/env python

from unittest import TestCase
import unittest

from inkex.colors import Color, ColorError, is_color

class ColorTest(TestCase):
    """Test for single transformations"""
    def test_empty(self):
        """Empty color (black)"""
        self.assertEqual(Color(), [0, 0, 0])

    def test_errors(self):
        """Color parsing errors"""
        self.assertRaises(ColorError, Color, {})
        self.assertRaises(ValueError, Color, [0, 0, 0, 0])
        self.assertRaises(ColorError, Color(None, space='nop').__str__)
        self.assertRaises(ColorError, Color(None, space='nop').to_rgb)
        self.assertRaises(ColorError, Color(None, space='nop').to_hsl)

    def test_namedcolor(self):
        """Named Color"""
        self.assertEqual(Color('red'), [255, 0, 0])
        self.assertEqual(str(Color('red')), '#ff0000')

    def test_rgb_hex(self):
        """RGB Hex Color"""
        color = Color('#ff0102')
        self.assertEqual(color, [255, 1, 2])
        self.assertEqual(str(color), '#ff0102')
        self.assertEqual(color.red, 255)
        self.assertEqual(color.green, 1)
        self.assertEqual(color.blue, 2)
        self.assertEqual(color.to_hsl(), [254, 255, 128])
        self.assertEqual(color.hue, 254)
        self.assertEqual(color.saturation, 255)
        self.assertEqual(color.lightness, 128)

    def test_rgb_to_hsl(self):
        """RGB to HSL Color"""
        self.assertEqual(Color('#ff7c7d').to_hsl(), [254, 255, 189])
        self.assertEqual(Color('#7e7c7d').to_hsl(), [233, 2, 125])
        self.assertEqual(Color('#7e7cff').to_hsl(), [170, 255, 189])
        self.assertEqual(Color('#7eff7d').to_hsl(), [84, 255, 190])

    def test_rgb_short_hex(self):
        """RGB Short Hex Color"""
        self.assertEqual(Color('#fff'), [255, 255, 255])
        self.assertEqual(str(Color('#fff')), '#ffffff')

    def test_rgb_int(self):
        """RGB Integer Color"""
        self.assertEqual(Color('rgb(255,255,255)'), [255, 255, 255])

    def test_rgb_percent(self):
        """RGB Percent Color"""
        self.assertEqual(Color('rgb(100%,100%,100%)'), [255, 255, 255])
        self.assertEqual(Color('rgb(50%,0%,1%)'), [127, 0, 2])
        self.assertEqual(Color('rgb(66.667%,0%,6.667%)'), [170, 0, 17])

    def test_hsl_color(self):
        """Parse HSL colors"""
        color = Color('hsl(4.0, 128, 99)')
        self.assertEqual(color, [4, 128, 99])
        self.assertEqual(str(color), 'hsl(4, 128, 99)')
        self.assertEqual(color.hue, 4)
        self.assertEqual(color.saturation, 128)
        self.assertEqual(color.lightness, 99)

    def test_hsl_to_rgb(self):
        """Convert HSL to RGB"""
        color = Color('hsl(172, 131, 128)')
        self.assertEqual(color.to_rgb(), [68, 62, 193])
        self.assertEqual(str(color.to_rgb()), '#443ec1')
        self.assertEqual(color.red, 68)
        self.assertEqual(color.green, 62)
        self.assertEqual(color.blue, 193)
        color = Color('hsl(172, 131, 10)')
        self.assertEqual(color.to_rgb(), [5, 4, 15])
        color = Color('hsl(0, 131, 10)')
        self.assertEqual(color.to_rgb(), [15, 4, 4])

    def test_hsl_grey(self):
        """Parse HSL Grey"""
        color = Color('hsl(172, 0, 128)')
        self.assertEqual(color.to_rgb(), [128, 128, 128])
        color = Color('rgb(128, 128, 128)')
        self.assertEqual(color.to_hsl(), [0, 0, 128])

    def test_is_color(self):
        """Can detect colour format"""
        self.assertFalse(is_color("rgb[t, b, s]"))
        self.assertTrue(is_color('#fff'))

if __name__ == '__main__':
    unittest.main()
