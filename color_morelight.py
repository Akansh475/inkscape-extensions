#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect
from inkex import colors

class MoreLight(coloreffect.ColorEffect):
    """Lighten selected objects"""
    def colmod(self, r, g, b):
        hsl = colors.rgb_to_hsl(r / 255, g / 255, b / 255)
        hsl[2] += 0.05
        if hsl[2] > 1.0:
            hsl[2] = 1.0
        rgb = colors.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
        return '{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

if __name__ == '__main__':
    MoreLight().run()
