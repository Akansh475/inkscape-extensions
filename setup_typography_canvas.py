#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2011 Felipe Correa da Silva Sanches
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import inkex
from inkex.elements import Guide

class SetupTypographyCanvas(inkex.Effect):
    def __init__(self):
        super(SetupTypographyCanvas, self).__init__()
        self.arg_parser.add_argument("-e", "--emsize",
                                     type=int,
                                     dest="emsize", default=1000,
                                     help="Em-size")
        self.arg_parser.add_argument("-a", "--ascender",
                                     type=int,
                                     dest="ascender", default='750',
                                     help="Ascender")
        self.arg_parser.add_argument("-c", "--caps",
                                     type=int,
                                     dest="caps", default='700',
                                     help="Caps Height")
        self.arg_parser.add_argument("-x", "--xheight",
                                     type=int,
                                     dest="xheight", default='500',
                                     help="x-height")
        self.arg_parser.add_argument("-d", "--descender",
                                     type=int,
                                     dest="descender", default='250',
                                     help="Descender")

    def create_horizontal_guideline(self, name, position):
        return self.svg.add(Guide().move_to(0, position, (0, 1)).update(inkscape__label=name))

    def create_vertical_guideline(self, name, position):
        return self.svg.add(Guide().move_to(position, 0, (1, 0)).update(inkscape__label=name))

    def effect(self):
        # Get all the options
        emsize = self.options.emsize
        ascender = self.options.ascender
        caps = self.options.caps
        xheight = self.options.xheight
        descender = self.options.descender

        # Get access to main SVG document element
        self.svg = self.document.getroot()
        self.svg.set("width", str(emsize))
        self.svg.set("height", str(emsize))
        self.svg.set("viewBox", "0 0 " + str(emsize) + " " + str(emsize))

        baseline = descender
        # Create guidelines
        self.create_horizontal_guideline("baseline", baseline)
        self.create_horizontal_guideline("ascender", baseline + ascender)
        self.create_horizontal_guideline("caps", baseline + caps)
        self.create_horizontal_guideline("xheight", baseline + xheight)
        self.create_horizontal_guideline("descender", baseline - descender)

        namedview = self.svg.find(inkex.addNS('namedview', 'sodipodi'))
        namedview.set(inkex.addNS('document-units', 'inkscape'), 'px')
        namedview.set(inkex.addNS('cx', 'inkscape'), str(emsize / 2.0))
        namedview.set(inkex.addNS('cy', 'inkscape'), str(emsize / 2.0))


if __name__ == '__main__':
    SetupTypographyCanvas().run()
