#!/usr/bin/env python

# Written by Tavmjong Bah

import inkex

class DvdCover(inkex.Effect):
    """Create an empty DVD Cover"""
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("-s", "--spine", type=float, dest="dvd_cover_spine",
                                     default="14", help="Dvd spine width (mm)")
        self.arg_parser.add_argument("-b", "--bleed", type=float, dest="dvd_cover_bleed",
                                     default="3", help="Bleed (extra area around image")

    def create_horizontal_guideline(self, name, position):
        self.create_guideline(name, "0,1", 0, position)

    def create_vertical_guideline(self, name, position):
        self.create_guideline(name, "1,0", position, 0)

    def create_guideline(self, label, orientation, x,y):
        namedview = self.root.find(inkex.addNS('namedview', 'sodipodi'))
        guide = inkex.etree.SubElement(namedview, inkex.addNS('guide', 'sodipodi'))
        guide.set("orientation", orientation)
        guide.set("position", str(x)+","+str(y))
        # No need to set label (causes translation problems, etc.)
        # guide.set(inkex.addNS('label', 'inkscape'), label)

    def effect(self):

        # Dimensions in mm
        width = 259.0 # Before adding spine width or bleed
        height = 183.0 # Before adding bleed

        bleed = self.options.dvd_cover_bleed
        spine = float(self.options.dvd_cover_spine)

        width += spine
        width += 2.0 * bleed
        height += 2.0 * bleed

        self.root = self.document.getroot()
        self.root.set("id", "SVGRoot")
        self.root.set("width", str(width) + 'mm')
        self.root.set("height", str(height) + 'mm')
        self.root.set("viewBox", "0 0 " + str(width) + " " + str(height) )

        namedview = self.root.find(inkex.addNS('namedview', 'sodipodi'))
        if namedview is None:
            namedview = inkex.etree.SubElement(self.root, inkex.addNS('namedview', 'sodipodi'))
         
        namedview.set(inkex.addNS('document-units', 'inkscape'), "mm")

        # Until units are supported in 'cx', etc.
        namedview.set(inkex.addNS('cx', 'inkscape'), str(self.svg.uutounit(width, 'px')/2.0))
        namedview.set(inkex.addNS('cy', 'inkscape'), str(self.svg.uutounit(height, 'px')/2.0))

        self.create_horizontal_guideline("bottom", str(self.svg.uutounit(bleed, 'px')))
        self.create_horizontal_guideline("top", str(self.svg.uutounit(height-bleed, 'px')))
        self.create_vertical_guideline("left edge", str(self.svg.uutounit(bleed, 'px')))
        self.create_vertical_guideline("left spline", str(self.svg.uutounit((width-spine)/2.0, 'px')))
        self.create_vertical_guideline("right spline", str(self.svg.uutounit((width+spine)/2.0, 'px')))
        self.create_vertical_guideline("left edge", str(self.svg.uutounit(width-bleed, 'px')))

if __name__ == '__main__':
    DvdCover().run()
