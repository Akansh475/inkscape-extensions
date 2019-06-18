#!/usr/bin/env python
# coding=utf-8

# Written by Tavmjong Bah
from __future__ import absolute_import, print_function, unicode_literals

import inkex

class GenericTemplate(inkex.EffectExtension):
    def __init__(self):
        super(GenericTemplate, self).__init__()
        self.arg_parser.add_argument("-w", "--width", type=int, dest="generic_width", default="1920", help="Custom width")
        self.arg_parser.add_argument("-z", "--height", type=int, dest="generic_height", default="1080", help="Custom height")
        self.arg_parser.add_argument("-u", "--unit", type=str, dest="generic_unit", default="px", help="SVG Unit")
        self.arg_parser.add_argument("-b", "--background", type=str, dest="generic_background", default="normal", help="Canvas background")
        self.arg_parser.add_argument("-n", "--noborder", type=inkex.inkbool, dest="generic_noborder", default=False)
        # self.arg_parser.add_argument("-l", "--layer", type=inkex.inkbool, dest="generic_layer", default=True)

    def effect(self):

        width = self.options.generic_width
        height = self.options.generic_height
        unit = self.options.generic_unit

        root = self.svg
        root.set("id", "SVGRoot")
        root.set("width", str(width) + unit)
        root.set("height", str(height) + unit)
        root.set("viewBox", "0 0 " + str(width) + " " + str(height))

        namedview = root.namedview
        namedview.set(inkex.addNS('document-units', 'inkscape'), unit)

        # Until units are supported in 'cx', etc.
        namedview.set(inkex.addNS('zoom', 'inkscape'), str(512.0 / self.svg.uutounit(width, 'px')))
        namedview.set(inkex.addNS('cx', 'inkscape'), str(self.svg.uutounit(width, 'px') / 2.0))
        namedview.set(inkex.addNS('cy', 'inkscape'), str(self.svg.uutounit(height, 'px') / 2.0))

        if self.options.generic_background == "white":
            namedview.set('pagecolor', "#ffffff")
            namedview.set('bordercolor', "#666666")
            namedview.set(inkex.addNS('pageopacity', 'inkscape'), "1.0")
            namedview.set(inkex.addNS('pageshadow', 'inkscape'), "0")

        if self.options.generic_background == "gray":
            namedview.set('pagecolor', "#808080")
            namedview.set('bordercolor', "#444444")
            namedview.set(inkex.addNS('pageopacity', 'inkscape'), "1.0")
            namedview.set(inkex.addNS('pageshadow', 'inkscape'), "0")

        if self.options.generic_background == "black":
            namedview.set('pagecolor', "#000000")
            namedview.set('bordercolor', "#999999")
            namedview.set(inkex.addNS('pageopacity', 'inkscape'), "1.0")
            namedview.set(inkex.addNS('pageshadow', 'inkscape'), "0")

        if self.options.generic_noborder:
            pagecolor = namedview.get('pagecolor')
            namedview.set('bordercolor', pagecolor)
            namedview.set('borderopacity', "0")

        # This needs more thought... we need to set "Current layer" to (root), how?
        # if self.options.generic_layer:
        #     # Add layer
        #     inkex.debug( "We want a layer" )
        # else:
        #     # Remove layer id default document (assuming only one)
        #     inkex.debug( "We don't want a layer" )
        #     layer_node = self.current_layer
        #     if layer_node is not None:
        #         inkex.debug( "We have layer" )
        #         root.remove(layer_node)
        #         try:
        #             del namedview.attrib[ inkex.addNS('current-layer', 'inkscape') ]
        #         except:
        #             pass


if __name__ == '__main__':
    GenericTemplate().run()
