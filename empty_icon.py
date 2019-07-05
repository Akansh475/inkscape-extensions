#!/usr/bin/env python
# coding=utf-8

# Written by Tavmjong Bah

import inkex

class EmptyIcon(inkex.EffectExtension):
    """Empty Icon Template"""

    def __init__(self):
        super(EmptyIcon, self).__init__()
        self.arg_parser.add_argument("-s", "--size", type=int, dest="icon_size",
                                     default="16", help="Icon size")

    def effect(self):

        size = self.options.icon_size

        root = self.document.getroot()
        root.set("id", "SVGRoot")
        root.set("width", str(size) + 'px')
        root.set("height", str(size) + 'px')
        root.set("viewBox", "0 0 " + str(size) + " " + str(size))

        namedview = self.svg.namedview
        namedview.set(inkex.addNS('document-units', 'inkscape'), 'px')

        namedview.set(inkex.addNS('zoom', 'inkscape'), str(256.0 / size))
        namedview.set(inkex.addNS('cx', 'inkscape'), str(size / 2.0))
        namedview.set(inkex.addNS('cy', 'inkscape'), str(size / 2.0))
        namedview.set(inkex.addNS('grid-bbox', 'inkscape'), "true")


if __name__ == '__main__':
    EmptyIcon().run()
