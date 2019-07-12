#!/usr/bin/env python
# coding=utf-8

# Rewritten by Tavmjong Bah to add correct viewBox, inkscape:cx, etc. attributes

import inkex

class EmptyPage(inkex.EffectExtension):
    """An empty page extension"""

    def __init__(self):
        super(EmptyPage, self).__init__()
        self.arg_parser.add_argument("-s", "--size", type=str, dest="page_size",
                                     default="a4", help="Page size")

    def effect(self):
        width = 300
        height = 300
        units = 'px'

        if self.options.page_size == "dl":
            width = 220
            height = 110
            units = 'mm'

        if self.options.page_size == "no10":
            width = 9.5
            height = 4.125
            units = 'in'

        root = self.document.getroot()
        root.set("id", "SVGRoot")
        root.set("width", str(width) + units)
        root.set("height", str(height) + units)
        root.set("viewBox", "0 0 " + str(width) + " " + str(height))

        namedview = self.svg.namedview
        namedview.set(inkex.addNS('document-units', 'inkscape'), units)

        # Until units are supported in 'cx', etc.
        namedview.set(inkex.addNS('cx', 'inkscape'), str(self.svg.uutounit(width, 'px') / 2.0))
        namedview.set(inkex.addNS('cy', 'inkscape'), str(self.svg.uutounit(height, 'px') / 2.0))


if __name__ == '__main__':
    EmptyPage().run()
