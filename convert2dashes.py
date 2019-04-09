#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2005,2007 Aaron Spike, aaron@ekips.org
# Copyright (C) 2009 Alvin Penner, penner@vaxxine.com
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
"""
This extension converts a path into a dashed line using 'stroke-dasharray'
It is a modification of the file addnodes.py
"""
import inkex

class Dashit(inkex.Effect):
    def __init__(self):
        super(Dashit, self).__init__()
        self.not_converted = []

    def effect(self):
        for i, node in self.svg.selected.items():
            self.convert2dash(node)
        if len(self.not_converted):
            inkex.errormsg(_('Total number of objects not converted: {}\n').format(len(self.not_converted)))
            # return list of IDs in case the user needs to find a specific object
            inkex.debug(self.not_converted)

    def convert2dash(self, node):
        if node.tag == inkex.addNS('g', 'svg'):
            for child in node:
                self.convert2dash(child)
        else:
            if node.tag == inkex.addNS('path','svg'):
                dashes = []
                offset = 0
                style = dict(inkex.Style.parse_str(node.get('style')))
                if 'stroke-dasharray' in style:
                    if style['stroke-dasharray'].find(',') > 0:
                        dashes = [float (dash) for dash in style['stroke-dasharray'].split(',')]
                if 'stroke-dashoffset' in style:
                    offset = style['stroke-dashoffset']
                if dashes:
                    p = inkex.parseCubicPath(node.get('d'))
                    new = []
                    for sub in p:
                        idash = 0
                        dash = dashes[0]
                        length = float (offset)
                        while dash < length:
                            length = length - dash
                            idash = (idash + 1) % len(dashes)
                            dash = dashes[idash]
                        new.append([sub[0][:]])
                        i = 1
                        while i < len(sub):
                            dash = dash - length
                            length = inkex.cspseglength(new[-1][-1], sub[i])
                            while dash < length:
                                new[-1][-1], next, sub[i] = inkex.cspbezsplitatlength(new[-1][-1], sub[i], dash/length)
                                if idash % 2:           # create a gap
                                    new.append([next[:]])
                                else:                   # splice the curve
                                    new[-1].append(next[:])
                                length = length - dash
                                idash = (idash + 1) % len(dashes)
                                dash = dashes[idash]
                            if idash % 2:
                                new.append([sub[i]])
                            else:
                                new[-1].append(sub[i])
                            i += 1
                    node.set('d', inkex.formatCubicPath(new))
                    del style['stroke-dasharray']
                    node.set('style', str(inkex.Style(style)))
                    if node.get(inkex.addNS('type','sodipodi')):
                        del node.attrib[inkex.addNS('type', 'sodipodi')]
            else:
                self.not_converted.append(node.get('id'))


if __name__ == '__main__':
    Dashit().run()

