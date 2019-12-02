#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect

class BlackAndWhite(coloreffect.ColorEffect):
    """Convert colours to black and white"""
    def add_arguments(self, pars):
        pars.add_argument("-t", "--threshold", type=int, default=127, help="Threshold Color Level")

    def colmod(self, r, g, b):
        # ITU-R Recommendation BT.709
        # l = 0.2125 * r + 0.7154 * g + 0.0721 * b

        # NTSC and PAL
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        grey = 255 if lum > self.options.threshold else 0
        return '{:02x}{:02x}{:02x}'.format(grey, grey, grey)

if __name__ == '__main__':
    BlackAndWhite().run()
