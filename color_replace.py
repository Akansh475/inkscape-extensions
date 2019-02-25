#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import coloreffect


class C(coloreffect.ColorEffect):
    """
    Replace color in SVG with another
    """

    def __init__(self):
        super(C, self).__init__()
        self.arg_parser.add_argument("-f", "--from_color",
                                     default="000000", help="Replace color")
        self.arg_parser.add_argument("-t", "--to_color",
                                     default="000000", help="By color")

    def colmod(self, r, g, b):
        this_color = '{:02x}{:02x}{:02x}'.format(r, g, b)

        from_color = self.options.from_color.strip('"').replace('#', '').lower().strip()
        to_color = self.options.to_color.strip('"').replace('#', '').lower().strip()

        if this_color == from_color:
            return to_color
        else:
            return this_color


if __name__ == '__main__':
    c = C()
    c.run()
