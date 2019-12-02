#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import random

import coloreffect
import inkex
from inkex import colors

class HslAdjust(coloreffect.ColorEffect):
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("-x", "--hue", type=int, default=0, help="Adjust hue")
        pars.add_argument("-s", "--saturation", type=int, default=0, help="Adjust saturation")
        pars.add_argument("-l", "--lightness", type=int, default=0, help="Adjust lightness")
        pars.add_argument("--random_h", type=inkex.Boolean, dest="random_hue")
        pars.add_argument("--random_s", type=inkex.Boolean, dest="random_saturation")
        pars.add_argument("--random_l", type=inkex.Boolean, dest="random_lightness")

    def clamp(self, minimum, x, maximum):
        return max(minimum, min(x, maximum))

    def colmod(self, r, g, b):
        hsl = colors.rgb_to_hsl(r / 255, g / 255, b / 255)

        if self.options.random_hue:
            hsl[0] = random.random()
        elif self.options.hue:
            hue_val = hsl[0] + (self.options.hue / 360)
            # Only return the fractional amount (i.e. 3.25 -> 0.25)
            hsl[0] = hue_val % 1

        if self.options.random_saturation:
            hsl[1] = random.random()
        elif self.options.saturation:
            sat_val = hsl[1] + (self.options.saturation / 100)
            hsl[1] = self.clamp(0, sat_val, 1)

        if self.options.random_lightness:
            hsl[2] = random.random()
        elif self.options.lightness:
            light_val = hsl[2] + (self.options.lightness / 100)
            hsl[2] = self.clamp(0, light_val, 1)

        rgb = colors.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
        return '{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


if __name__ == '__main__':
    HslAdjust().run()
