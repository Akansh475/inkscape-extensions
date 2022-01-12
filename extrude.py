#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2022 Jonathan Neuhauser, jonathan.neuhauser@outlook.com
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


import itertools
from typing import List, Union

import inkex
from inkex.localization import inkex_gettext as _
class _SubpathManager:
    def __init__(self, style):
        self.current = inkex.Path()
        self.style = style
    def add(self, command: Union[inkex.paths.PathCommand, List[inkex.paths.PathCommand]]):
        """Add a path command"""
        self.current.append(command)
    def terminate(self):
        """Terminate current subpath"""
    def append_next(self, sibling_before: inkex.BaseElement):
        """Append result as sibling after given element"""
        pth = inkex.PathElement()
        pth.path = self.current
        pth.style = self.style
        sibling_before.addnext(pth)

class _GroupManager(_SubpathManager):
    def __init__(self, style):
        super().__init__(style)
        self.result = inkex.Group()
    def terminate(self):
        if len(self.current) > 1:
            pth = inkex.PathElement()
            pth.path = self.current.to_absolute()
            pth.style = self.style
            self.result.append(pth)
        self.current = inkex.Path()
    def append_next(self, sibling_before: inkex.BaseElement):
        sibling_before.addnext(self.result)


class Extrude(inkex.EffectExtension):
    """This effect draws lines between each nth node of each selected path.
    It can be chosen whether these regions are filled and whether the fill uses rectangles
    or copies of the path segments.
    The lines will be inserted between the two elements.
    """
    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("-m", "--mode", default="lines", choices=["lines", "polygons", "snug"],
         help="Join paths with lines, polygons or copies of the segments (\"snug\")")
        pars.add_argument("-s", "--subpaths", default=True, type=inkex.Boolean,
         help="""If true, connecting lines will be inserted as subpaths of a single path.
                 If false, they will be inserted in newly created group. 
                 Only applies to mode=lines""")
    @staticmethod
    def _handle_snug(manager, com1, com2):
        manager.add(inkex.paths.Move(*com1.previous_end_point))
        com1r = com1.command
        com2r = com2.reverse()
        doflag = True
        if isinstance(com1r, (inkex.paths.ZoneClose, inkex.paths.zoneClose)):
            # ZoneClose can not be used directly, must be converted to line
            com1r = inkex.paths.Line(*com1.first_point)
            if com1.previous_end_point.is_close(com1.end_point):
                doflag = False
        if doflag:
            manager.add([com1r, inkex.paths.Line(*com2.end_point),
                        com2r, inkex.paths.ZoneClose()])
    def effect(self):
        paths : List[inkex.PathElement] = []
        for node in self.svg.selection.rendering_order().filter(inkex.ShapeElement):
            if isinstance(node, inkex.PathElement):
                node.apply_transform()
            paths.append(node)
        if len(paths) < 2:
            raise inkex.AbortExtension(_("Need at least 2 paths selected"))

        mode = self.options.mode.lower()
        subpaths = self.options.subpaths and mode == "lines"

        if mode == 'lines':
            style = {
                'fill': 'none',
                'stroke': '#000000',
                'stroke-opacity': 1,
                'stroke-width': '1px',
            }
        elif mode in ('polygons', 'snug'):
            style = {
                'fill': '#000000',
                'fill-opacity': 0.3,
                'stroke': '#000000',
                'stroke-opacity': 0.6,
                'stroke-width': '1px',
                'stroke-linejoin': 'round'
            }

        for pa1, pa2 in itertools.combinations(paths, 2):
            manager = _SubpathManager(style) if subpaths else _GroupManager(style)
            for com1, com2 in zip(pa1.path.proxy_iterator(), pa2.path.proxy_iterator()):

                if (mode == "lines" and
                   not (isinstance(com1.command, (inkex.paths.ZoneClose, inkex.paths.zoneClose)) or
                        isinstance(com2.command, (inkex.paths.ZoneClose, inkex.paths.zoneClose)))):
                        # For a closed subpath, the first line has already been drawn.
                    manager.add(inkex.paths.Move(*com1.end_point))
                    manager.add(inkex.paths.Line(*com2.end_point))
                if not (isinstance(com1.command, (inkex.paths.Move, inkex.paths.move)) or
                        isinstance(com2.command, (inkex.paths.Move, inkex.paths.move))):
                    # We skip if one of either commands is a "Move" command
                    if mode == "polygons":
                        manager.add(inkex.paths.Move(*com1.previous_end_point))
                        manager.add([inkex.paths.Line(*pt) for pt in
                                      [com1.end_point, com2.end_point,
                                       com2.previous_end_point, com1.previous_end_point]])
                    if mode == "snug":
                        Extrude._handle_snug(manager, com1, com2)
                manager.terminate()
            manager.append_next(pa1)



if __name__ == '__main__':
    Extrude().run()
