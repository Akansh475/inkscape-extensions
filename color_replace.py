#!/usr/bin/env python
import coloreffect

import inkex

class C(coloreffect.ColorEffect):
    def __init__(self):
        coloreffect.ColorEffect.__init__(self)
        self.arg_parser.add_argument("-f", "--from_color",
                default="000000", help="Replace color")
        self.arg_parser.add_argument("-t", "--to_color",
                default="000000", help="By color")

    def colmod(self,r,g,b):
        this_color = '%02x%02x%02x' % (r, g, b)

        fr = self.options.from_color.strip('"').replace('#', '').lower()
        to = self.options.to_color.strip('"').replace('#', '').lower()
             
        #inkex.debug(this_color+"|"+fr+"|"+to)
        if this_color == fr:
            return to
        else:
            return this_color

if __name__ == '__main__':
    c = C()
    c.affect()
