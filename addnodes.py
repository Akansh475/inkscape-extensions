#!/usr/bin/env python
# coding=utf-8
#
# This extension either adds nodes to a path so that
#    a) no segment is longer than a maximum value
#    or
#    b) so that each segment is divided into a given number of equal segments
#
# Copyright (C) 2005, 2007 Aaron Spike, aaron@ekips.org
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

import math

import inkex
from inkex.base import InkscapeExtension, SvgThroughMixin


class SplitIt(SvgThroughMixin, InkscapeExtension):
    def __init__(self):
        super(SplitIt, self).__init__()
        self.arg_parser.add_argument("--segments",
                                     type=int,
                                     dest="segments", default=2,
                                     help="Number of segments to divide the path into")
        self.arg_parser.add_argument("--max",
                                     type=float,
                                     dest="max", default=2,
                                     help="Number of segments to divide the path into")
        self.arg_parser.add_argument("--method",
                                     type=str,
                                     dest="method", default='',
                                     help="The kind of division to perform")

    def effect(self):

        for id, node in self.svg.selected.items():
            if node.tag == inkex.addNS('path', 'svg'):
                d = node.get('d')
                p = inkex.parseCubicPath(d)

                new = []
                for sub in p:
                    new.append([sub[0][:]])
                    i = 1
                    while i <= len(sub) - 1:
                        length = inkex.cspseglength(new[-1][-1], sub[i])

                        if self.options.method == 'bynum':
                            splits = self.options.segments
                        else:
                            splits = math.ceil(length / self.options.max)

                        for s in range(int(splits), 1, -1):
                            result = inkex.cspbezsplitatlength(new[-1][-1], sub[i], 1.0 / s)
                            better_result = [[list(_) for _ in elements] for elements in result]
                            new[-1][-1], next, sub[i] = better_result
                            new[-1].append(next[:])
                        new[-1].append(sub[i])
                        i += 1
                node.set('d', inkex.formatCubicPath(new))


if __name__ == '__main__':
    SplitIt().run()
