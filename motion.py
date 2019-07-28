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
from inkex.paths import Move, Line, Curve, ZoneClose
from inkex.bezier import beziertatslope, beziersplitatt

class Motion(inkex.EffectExtension):
    """Generate a motion path"""
    def add_arguments(self, pars):
        pars.add_argument("-a", "--angle", type=float, default=45.0,\
             help="direction of the motion vector")
        pars.add_argument("-m", "--magnitude", type=float, default=100.0,\
             help="magnitude of the motion vector")

    @staticmethod
    def makeface(last, segment, facegroup, delx, dely):
        """translate path segment along vector"""
        elem = facegroup.add(inkex.PathElement())

        npt = segment.translate([delx, dely])

        # reverse direction of path segment
        rev = list(npt.args)
        rev[-2:] = last[0] + delx, last[1] + dely
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
        delx = math.cos(math.radians(self.options.angle)) * self.options.magnitude
        dely = math.sin(math.radians(self.options.angle)) * self.options.magnitude
        last = None
        for node in self.svg.selected.values():
            if isinstance(node, inkex.PathElement):
                group = node.getparent().add(inkex.Group())
                facegroup = group.add(inkex.Group())
                group.append(node)

                if node.transform:
                    group.transform = node.transform
                    node.transform = None

                facegroup.style = node.style

                for segment in node.path.to_absolute():
                    self.process_segment(last, segment, facegroup, delx, dely)

                    if isinstance(segment, Move):
                        path_start = (segment.x, segment.y)
                    if isinstance(segment, ZoneClose):
                        last = path_start
                    else:
                        last = segment.end_point(None, None)

    @staticmethod
    def process_segment(last, segment, facegroup, delx, dely):
        """Process each segments"""
        tees = []
        if isinstance(segment, Curve):
            bez = [last] + segment.to_bez()
            tees = [t for t in beziertatslope(bez, (dely, delx)) if 0 < t < 1]
            tees.sort()

        segments = []
        if not tees and isinstance(segment, (Line, Curve)):
            segments.append(segment)
        elif len(tees) == 1:
            one, two = beziersplitatt(bez, tees[0])
            segments.append(Curve(*(one[1] + one[2] + one[3])))
            segments.append(Curve(*(two[1] + two[2] + two[3])))
        elif len(tees) == 2:
            one, two = beziersplitatt(bez, tees[0])
            two, three = beziersplitatt(two, tees[1])
            segments.append(Curve(*(one[1] + one[2] + one[3])))
            segments.append(Curve(*(two[1] + two[2] + two[3])))
            segments.append(Curve(*(three[1] + three[2] + three[3])))

        for seg in segments:
            Motion.makeface(last, seg, facegroup, delx, dely)
            last = segment.end_point(None, None)


if __name__ == '__main__':
    Motion().run()
