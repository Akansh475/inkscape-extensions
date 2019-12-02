#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import random

import coloreffect
from inkex import colors

class Randomize(coloreffect.ColorEffect):
    """Randomize the colours of all objects"""
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("-y", "--hue_range", type=int, default=0, help="Hue range")
        pars.add_argument("-t", "--saturation_range", type=int, default=0, help="Saturation range")
        pars.add_argument("-m", "--lightness_range", type=int, default=0, help="Lightness range")
        pars.add_argument("-o", "--opacity_range", type=int, default=0, help="Opacity range")

    def randomize_hsl(self, limit, current_value):
        limit = 255 * float(limit) / 100
        limit /= 2
        max_ = int((current_value * 255) + limit)
        min_ = int((current_value * 255) - limit)
        if max_ > 255:
            min_ -= max_ - 255
            max_ = 255
        if min_ < 0:
            max_ -= min_
            min_ = 0
        return random.randrange(min_, max_) / 255

    def colmod(self, r, g, b):
        hsl = colors.rgb_to_hsl(r / 255, g / 255, b / 255)
        if self.options.hue_range > 0:
            hsl[0] = self.randomize_hsl(self.options.hue_range, hsl[0])
        if self.options.saturation_range > 0:
            hsl[1] = self.randomize_hsl(self.options.saturation_range, hsl[1])
        if self.options.lightness_range > 0:
            hsl[2] = self.randomize_hsl(self.options.lightness_range, hsl[2])
        rgb = colors.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
        return '{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def opacmod(self, opacity):
        if self.options.opacity_range > 0:
            # maybe not necessary, but better not change things that shouldn't change
            try:
                opacity = float(opacity)
            except ValueError:
                return opacity

            limit = self.options.opacity_range
            limit /= 2
            max_ = opacity * 100 + limit
            min_ = opacity * 100 - limit
            if max_ > 100:
                min_ = min_ - (max_ - 100)
                max_ = 100
            if min_ < 0:
                max_ = max_ - min_
                min_ = 0
            ret = str(random.uniform(min_, max_) / 100)
            return ret
        return opacity

if __name__ == '__main__':
    Randomize().run()
