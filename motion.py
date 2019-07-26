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

import inkex
from inkex.paths import PathCommand, Move, Line, Curve, ZoneClose
from inkex.bezier import beziertatslope, beziersplitatt

class Motion(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("-a", "--angle", type=float, default=45.0,\
             help="direction of the motion vector")
        pars.add_argument("-m", "--magnitude", type=float, default=100.0,\
             help="magnitude of the motion vector")

    def makeface(self, last, segment):
        """translate path segment along vector"""
        elem = self.facegroup.add(inkex.PathElement())

        npt = segment.translate([self.vx, self.vy])

        # reverse direction of path segment
        rev = list(npt.args)
        rev[-2:] = last[0] + self.vx, last[1] + self.vy
        if isinstance(segment, Curve):
            rev = list(Curve(rev[2], rev[3], rev[0], rev[1], rev[4], rev[5]).args)
        rev = type(segment)(*rev)

        elem.path = inkex.Path([
            Move(*last),
            segment,
            npt.to_line(),
            rev,
            ZoneClose(),
        ])

    def effect(self):
        self.vx = math.cos(math.radians(self.options.angle)) * self.options.magnitude
        self.vy = math.sin(math.radians(self.options.angle)) * self.options.magnitude
        last = None
        for node in self.svg.selected.values():
            if isinstance(node, inkex.PathElement):
                group = node.getparent().add(inkex.Group())
                self.facegroup = group.add(inkex.Group())
                group.append(node)

                if node.transform:
                    group.transform = node.transform
                    node.transform = None

                self.facegroup.style = node.style

                for segment in node.path.to_absolute():
                    cmdcls = PathCommand.letter_to_class(segment.letter)
                    tees = []
                    if isinstance(segment, Curve):
                        bez = (last, segment[:2], segment[2:4], segment[-2:])
                        tees = [t for t in beziertatslope(bez, (self.vy, self.vx)) if 0 < t < 1]
                        tees.sort()

                    segments = []
                    if not tees and isinstance(segment, (Line, Curve)):
                        segments.append(segment)
                    elif len(tees) == 1:
                        one, two = beziersplitatt(bez, tees[0])
                        segments.append(cmdcls(one[1] + one[2] + one[3]))
                        segments.append(cmdcls(two[1] + two[2] + two[3]))
                    elif len(tees) == 2:
                        one, two = beziersplitatt(bez, tees[0])
                        two, three = beziersplitatt(two, tees[1])
                        segments.append(cmdcls(one[1] + one[2] + one[3]))
                        segments.append(cmdcls(two[1] + two[2] + two[3]))
                        segments.append(cmdcls(three[1] + three[2] + three[3]))

                    for seg in segments:
                        self.makeface(last, seg)
                        last = seg.x, seg.y

                    if isinstance(segment, Move):
                        path_start = (segment.x, segment.y)
                    if isinstance(segment, ZoneClose):
                        last = path_start
                    else:
                        last = (segment.x, segment.y)


if __name__ == '__main__':
    Motion().run()
