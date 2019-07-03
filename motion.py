#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
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

import math

from lxml import etree

import inkex
from inkex.paths import PathCommand, Curve

class Motion(inkex.Effect):
    def __init__(self):
        super(Motion, self).__init__()
        self.arg_parser.add_argument("-a", "--angle",
                                     type=float,
                                     dest="angle", default=45.0,
                                     help="direction of the motion vector")
        self.arg_parser.add_argument("-m", "--magnitude",
                                     type=float,
                                     dest="magnitude", default=100.0,
                                     help="magnitude of the motion vector")

    def makeface(self, last, segment):
        """translate path segment along vector"""
        a = []
        a.append(['M', last[:]])
        a.append([segment.letter, list(segment.args)])

        npt = segment.translate([self.vx, self.vy])
        #defs = simplepath.pathdefs[cmd]
        #for i in range(defs[1]):
        #        np[i] += self.vx
        #    elif defs[3][i] == 'y':
        #        np[i] += self.vy

        a.append(['L', [npt.x, npt.y]])

        # reverse direction of path segment
        npt = list(npt.args)
        npt[-2:] = last[0] + self.vx, last[1] + self.vy
        if segment.letter == 'C':
            npt = list(Curve(npt[2], npt[3], npt[0], npt[1], npt[4], npt[5]).args)
        a.append([segment.letter, npt])

        a.append(['Z', []])
        etree.SubElement(self.facegroup, inkex.addNS('path', 'svg'), {'d': str(inkex.Path(a))})

    def effect(self):
        self.vx = math.cos(math.radians(self.options.angle)) * self.options.magnitude
        self.vy = math.sin(math.radians(self.options.angle)) * self.options.magnitude
        last = None
        for id, node in self.svg.selected.items():
            if node.tag == inkex.addNS('path', 'svg'):
                group = etree.SubElement(node.getparent(), inkex.addNS('g', 'svg'))
                self.facegroup = etree.SubElement(group, inkex.addNS('g', 'svg'))
                group.append(node)

                t = node.get('transform')
                if t:
                    group.set('transform', t)
                    node.set('transform', '')

                s = node.get('style')
                self.facegroup.set('style', s)

                for segment in node.path:
                    cmdcls = PathCommand.letter_to_class(segment.letter)
                    tees = []
                    if segment.letter == 'C':
                        bez = (last, segment[:2], segment[2:4], segment[-2:])
                        tees = [t for t in inkex.beziertatslope(bez, (self.vy, self.vx)) if 0 < t < 1]
                        tees.sort()

                    segments = []
                    if len(tees) == 0 and segment.letter in ['L', 'C']:
                        segments.append(segment)
                    elif len(tees) == 1:
                        one, two = inkex.beziersplitatt(bez, tees[0])
                        segments.append(cmdcls(one[1] + one[2] + one[3]))
                        segments.append(cmdcls(two[1] + two[2] + two[3]))
                    elif len(tees) == 2:
                        one, two = inkex.beziersplitatt(bez, tees[0])
                        two, three = inkex.beziersplitatt(two, tees[1])
                        segments.append(cmdcls(one[1] + one[2] + one[3]))
                        segments.append(cmdcls(two[1] + two[2] + two[3]))
                        segments.append(cmdcls(three[1] + three[2] + three[3]))

                    for seg in segments:
                        self.makeface(last, seg)
                        last = seg.x, seg.y

                    if segment.letter == 'M':
                        subPathStart = (segment.x, segment.y)
                    if segment.letter == 'Z':
                        last = subPathStart
                    else:
                        last = (segment.x, segment.y)


if __name__ == '__main__':
    Motion().run()
