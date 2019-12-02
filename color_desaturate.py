#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect

class Desaturate(coloreffect.ColorEffect):
    """Remove colour but maintain intesity"""
    def colmod(self, r, g, b):
        lum = (max(r, g, b) + min(r, g, b)) // 2
        grey = int(round(lum))
        return '{:02x}{:02x}{:02x}'.format(grey, grey, grey)


if __name__ == '__main__':
    Desaturate().run()
