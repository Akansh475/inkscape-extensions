#!/usr/bin/env python
#
# Copyright (C) 2016 su_v, <suv-sf@users.sf.net>
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Convert path to mesh gradient
"""

import inkex
from inkex import BaseElement, Gradient
from inkex.paths import Line, Curve

class MeshGradient(Gradient):
    """Usable MeshGradient XML base class"""
    tag_name = 'meshgradient'

    @classmethod
    def new_mesh(cls, pos=None, rows=1, cols=1, autocollect=True):
        """Return skeleton of 1x1 meshgradient definition."""
        # initial point
        if pos is None or len(pos) != 2:
            pos = [0.0, 0.0]
        # create nested elements for rows x cols mesh
        meshgradient = cls()
        for _ in range(rows):
            meshrow = meshgradient.add(MeshRow())
            for _ in range(cols):
                meshrow.append(MeshPatch())
        # set meshgradient attributes
        meshgradient.set('gradientUnits', 'userSpaceOnUse')
        meshgradient.set('x', pos[0])
        meshgradient.set('y', pos[1])
        if autocollect:
            meshgradient.set('inkscape:collect', 'always')
        return meshgradient


class MeshRow(BaseElement):
    """Each row of a mesh gradient"""
    tag_name = 'meshrow'

class MeshPatch(BaseElement):
    """Each column or 'patch' in a mesh gradient"""
    tag_name = 'meshpatch'

    def stops(self, edges, colors):
        """Add or edit meshpatch stops with path and stop-color."""
        # iterate stops based on number of edges (path data)
        for i, edge in enumerate(edges):
            if i < len(self):
                stop = self[i]
            else:
                stop = self.add(MeshStop())

            # set edge path data
            stop.set('path', str(edge))
            # set stop color
            stop.style['stop-color'] = str(colors[i % 2])


class MeshStop(BaseElement):
    """Each stop color in a gradient"""
    tag_name = 'stop'


class PathToMesh(inkex.EffectExtension):
    """Convert path data to mesh geometry."""
    def add_arguments(self, pars):
        pars.add_argument("--tab", help="The selected UI-tab")

    def add_mesh(self, meshgradient):
        """Add meshgradient definition to current document."""
        self.svg.defs.append(meshgradient)
        meshgradient.set_random_id('meshgradient')
        return meshgradient.get_id()

    def effect(self):
        """Main routine to convert path data to mesh geometry."""
        # loop through selection
        for node in self.svg.get_selected(inkex.PathElement):
            csp = None
            meshgradient = None
            mesh_id = None
            # parse path data
            csp = node.path.to_superpath()
            # convert csp to meshgradient definition
            if csp is not None:
                # TODO: check length of path data / csp
                meshgradient = self.to_mesh(node, csp)
            # add meshgradient to document
            if meshgradient is not None:
                mesh_id = self.add_mesh(meshgradient)
            # apply meshgradient to node
            if mesh_id is not None:
                node.style['fill'] = 'url(#{})'.format(mesh_id)

    def to_mesh(self, node, csp, subpath=0):
        """Convert csp to meshgradient geometry."""
        # mesh data
        corners, edges = self.to_meshdata(csp[subpath])
        # alternating stop colors
        colors = [node.style.get('fill'), '#ffffff']
        # define meshgradient with first corner as initial point
        meshgradient = MeshGradient.new_mesh(pos=corners[0], rows=1, cols=1)
        # define stops (stop-color, path) for first meshpatch
        meshgradient[0][0].stops(edges[0:4], colors)
        return meshgradient

    @staticmethod
    def to_meshdata(subpath):
        """Convert csp subpath to corners, edge path data."""
        if len(subpath) >= 5:
            corners = []
            edges = []
            for i, corner in enumerate(subpath[:4]):
                corners.append(corner[1])
                edge = [list(subpath[i]), list(subpath[i+1])]
                edge[0][0] = list(edge[0][1])
                edge[1][2] = list(edge[1][1])
                if inkex.CubicSuperPath.is_line(edge[0], edge[1]):
                    edges.append(Line(*edge[1][1]))
                else:
                    edges.append(Curve(*(edge[0][2] + edge[1][0] + edge[1][1])))

        return corners, edges

if __name__ == '__main__':
    PathToMesh().run()
