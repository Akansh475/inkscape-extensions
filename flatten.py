#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2006 Aaron Spike, aaron@ekips.org
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
from inkex.elements import PathElement
from inkex.paths import Path
from inkex.generic import EffectExtension

class Flatten(EffectExtension):
    def __init__(self):
        super(Flatten, self).__init__()
        self.arg_parser.add_argument("-f", "--flatness",
                         type=float,
                        dest="flat", default=10.0,
                        help="Minimum flatness of the subdivided curves")
    def effect(self):
        for node in self.svg.selected.values():
            if isinstance(node, PathElement):
                d = node.get('d')
                p = inkex.parseCubicPath(d)
                inkex.cspsubdiv(p, self.options.flat)
                np = []
                for sp in p:
                    first = True
                    for csp in sp:
                        cmd = 'L'
                        if first:
                            cmd = 'M'
                        first = False
                        np.append([cmd,[csp[1][0],csp[1][1]]])
                node.set('d', str(Path(np)))

if __name__ == '__main__':
    Flatten().run()

