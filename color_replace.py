#!/usr/bin/env python
# coding=utf-8
"""Replace color extension"""
from __future__ import absolute_import, division

import coloreffect

class ReplaceColor(coloreffect.ColorEffect):
    """Replace color in SVG with another"""
    def add_arguments(self, pars):
        pars.add_argument("-f", "--from_color", default="000000", help="Replace color")
        pars.add_argument("-t", "--to_color", default="000000", help="By color")

    def colmod(self, r, g, b):
        this_color = '{:02x}{:02x}{:02x}'.format(r, g, b)

        from_color = self.options.from_color.strip('"').replace('#', '').lower().strip()
        to_color = self.options.to_color.strip('"').replace('#', '').lower().strip()

        if this_color == from_color:
            return to_color
        return this_color

if __name__ == '__main__':
    ReplaceColor().run()
