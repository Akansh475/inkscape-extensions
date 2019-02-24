#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect
import inkex


class C(coloreffect.ColorEffect):
    def colmod(self, r, g, b):
        hsl = inkex.rgb_to_hsl(r / 255, g / 255, b / 255)
        hsl[1] += 0.05
        if hsl[1] > 1.0:
            hsl[1] = 1.0
        rgb = inkex.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
        return '{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


if __name__ == '__main__':
    c = C()
    c.run()
