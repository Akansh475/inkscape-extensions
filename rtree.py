#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
# Copyright (C) 2015 su_v, suv-sf@users.sf.net
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

from lxml import etree

import inkex
from inkex import inkbool
from inkex import turtle as pturtle


class RTreeTurtle(inkex.Effect):
    def __init__(self):
        super(RTreeTurtle, self).__init__()
        self.arg_parser.add_argument("-s", "--size",
                                     type=float,
                                     dest="size", default=100.0,
                                     help="initial branch size")
        self.arg_parser.add_argument("-m", "--minimum",
                                     type=float,
                                     dest="minimum", default=4.0,
                                     help="minimum branch size")
        self.arg_parser.add_argument("--pentoggle",
                                     type=inkbool,
                                     dest="pentoggle", default=False,
                                     help="Lift pen for backward steps")

    def effect(self):
        self.options.size = self.svg.unittouu(str(self.options.size) + 'px')
        self.options.minimum = self.svg.unittouu(str(self.options.minimum) + 'px')
        s = {'stroke-linejoin': 'miter', 'stroke-width': str(self.svg.unittouu('1px')),
             'stroke-opacity': '1.0', 'fill-opacity': '1.0',
             'stroke': '#000000', 'stroke-linecap': 'butt',
             'fill': 'none'}
        t = pturtle.pTurtle()
        t.pu()
        point = self.svg.get_center_position()
        t.setpos(point)
        t.pd()
        t.rtree(self.options.size, self.options.minimum, self.options.pentoggle)

        attribs = {'d': t.getPath(), 'style': str(inkex.Style(s))}
        etree.SubElement(self.svg.get_current_layer(), inkex.addNS('path', 'svg'), attribs)


if __name__ == '__main__':
    RTreeTurtle().run()
