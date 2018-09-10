#!/usr/bin/env python

# standard library
import random
# local library
import coloreffect
import inkex

class C(coloreffect.ColorEffect):
    def __init__(self):
        coloreffect.ColorEffect.__init__(self)
        self.arg_parser.add_argument("-x", "--hue",
            type=int, default=0,
            help="Adjust hue")
        self.arg_parser.add_argument("-s", "--saturation",
            type=int, default=0,
            help="Adjust saturation")
        self.arg_parser.add_argument("-l", "--lightness",
            type=int, default=0,
            help="Adjust lightness")
        self.arg_parser.add_argument("--random_h",
            type=inkex.inkbool, 
            dest="random_hue", default=False,
            help="Randomize hue")
        self.arg_parser.add_argument("--random_s",
            type=inkex.inkbool, 
            dest="random_saturation", default=False,
            help="Randomize saturation")
        self.arg_parser.add_argument("--random_l",
            type=inkex.inkbool, 
            dest="random_lightness", default=False,
            help="Randomize lightness")
        self.arg_parser.add_argument("--tab",
            help="The selected UI-tab when OK was pressed")

    def clamp(self, minimum, x, maximum):
        return max(minimum, min(x, maximum))
        
    def colmod(self, r, g, b):
        hsl = inkex.rgb_to_hsl(r/255.0, g/255.0, b/255.0)
        #inkex.debug("hsl old: " + str(hsl[0]) + ", " + str(hsl[1]) + ", " + str(hsl[2]))
        if (self.options.random_hue):
            hsl[0] = random.random()
        elif (self.options.hue):
            hueval = hsl[0] + (self.options.hue / 360.0)
            hsl[0] = hueval % 1
        if(self.options.random_saturation):
            hsl[1] = random.random()
        elif (self.options.saturation):
            satval = hsl[1] + (self.options.saturation / 100.0)
            hsl[1] = self.clamp(0.0, satval, 1.0)
        if(self.options.random_lightness):
            hsl[2] = random.random()
        elif (self.options.lightness):
            lightval = hsl[2] + (self.options.lightness / 100.0)
            hsl[2] = self.clamp(0.0, lightval, 1.0)
        #inkex.debug("hsl new: " + str(hsl[0]) + ", " + str(hsl[1]) + ", " + str(hsl[2]))
        rgb = inkex.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
        return '%02x%02x%02x' % (rgb[0]*255, rgb[1]*255, rgb[2]*255)

c = C()
c.affect()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
