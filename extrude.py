#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2007
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
"""Join paths with lines or polygons"""

from lxml import etree

from inkex.localize import _

from inkex.cubic_paths import parseCubicPath, unCubicSuperPath
from inkex.elements import PathElement, Group
from inkex.paths import Path
import inkex


class Extrude(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        opts = [('-m', '--mode', str, 'mode', 'Lines',
                 'Join paths with lines or polygons'),
                ]
        for o in opts:
            self.arg_parser.add_argument(o[0], o[1], type=o[2],
                                         dest=o[3], default=o[4], help=o[5])

    def effect(self):
        paths = []
        for node in self.svg.selected.values():
            if isinstance(node, PathElement):
                paths.append(node)
        if len(paths) < 2:
            inkex.errormsg(_('Need at least 2 paths selected'))
            return

        for path in paths:
            path.apply_transform()

        pts = [parseCubicPath(node.path) for node in paths]

        for n1 in range(0, len(paths)):
            for n2 in range(n1 + 1, len(paths)):
                verts = []
                for i in range(0, min(map(len, pts))):
                    comp = []
                    for j in range(0, min(len(pts[n1][i]), len(pts[n2][i]))):
                        comp.append([pts[n1][i][j][1][-2:], pts[n2][i][j][1][-2:]])
                    verts.append(comp)

                if self.options.mode.lower() == 'lines':
                    line = []
                    for comp in verts:
                        for n, v in enumerate(comp):
                            line += [('M', v[0])]
                            line += [('L', v[1])]
                    ele = PathElement()
                    paths[0].xpath('..')[0].append(ele)
                    ele.set('d', str(Path(line)))
                    style = {
                        'fill': 'none',
                        'stroke': '#000000',
                        'stroke-opacity': 1,
                        'stroke-width': self.svg.unittouu('1px'),
                    }
                    ele.set('style', str(inkex.Style(style)))
                elif self.options.mode.lower() == 'polygons':
                    g = Group()
                    style = {
                        'fill': '#000000',
                        'fill-opacity': 0.3,
                        'stroke': '#000000',
                        'stroke-opacity': 0.6,
                        'stroke-width': self.svg.unittouu('2px'),
                    }
                    g.set('style', str(inkex.Style(style)))
                    paths[0].xpath('..')[0].append(g)
                    for comp in verts:
                        for n, v in enumerate(comp):
                            nn = n + 1
                            if nn == len(comp):
                                nn = 0
                            line = []
                            line += [('M', comp[n][0])]
                            line += [('L', comp[n][1])]
                            line += [('L', comp[nn][1])]
                            line += [('L', comp[nn][0])]
                            line += [('L', comp[n][0])]
                            ele = PathElement()
                            g.append(ele)
                            ele.set('d', str(Path(line)))


if __name__ == '__main__':
    Extrude().run()
