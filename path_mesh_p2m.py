#!/usr/bin/env python
"""
path_to_mesh - Convert path to meshgradient

Copyright (C) 2016 su_v, <suv-sf@users.sf.net>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
# local library
import inkex

# globals
MG_PROPS = [
    'fill',
    'stroke',
    'stop-color',
]


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    """Test approximate equality.

    ref:
        PEP 485 -- A Function for testing approximate equality
        https://www.python.org/dev/peps/pep-0485/#proposed-implementation
    """
    # pylint: disable=invalid-name
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def is_near_pt(pt1, pt2):
    """Test points for coincidence."""
    return isclose(pt1[0], pt2[0]) and isclose(pt1[1], pt2[1])


def is_line(segment):
    """Check whether csp segment (two points) has retracted handles."""
    return (is_near_pt(segment[0][1], segment[0][2]) and
            is_near_pt(segment[1][0], segment[1][1]))


def is_meshgradient(node):
    """Check whether linked node is meshgradient definition."""
    return (node.tag == inkex.addNS('meshgradient', 'svg') or
            node.tag == inkex.addNS('meshGradient', 'svg') or
            node.tag == inkex.addNS('mesh', 'svg'))


def is_path(node):
    """Check whether element type of *node* is <path>."""
    return (node.tag == inkex.addNS('path', 'svg') or
            node.tag == 'path')


def print_corners(corners):
    """Debug print coordinates of meshpatch corners."""
    inkex.debug('=== corners per row: ===')
    for row in corners:
        inkex.debug(row)


def format_point(point):
    """Format point coordinates for path data as string."""
    if len(point) == 2:
        return '{},{}'.format(*point)
    return '0.0,0.0'


def get_defs(node):
    """Find <defs> in children of *node*, return first one found."""
    path = '/svg:svg//svg:defs'
    try:
        return node.xpath(path, namespaces=inkex.NSS)[0]
    except IndexError:
        return inkex.etree.SubElement(node, inkex.addNS('defs', 'svg'))


def get_prop_color(node, prop='fill', default='#000000'):
    """Return style property *prop* of *node"."""
    color = ''
    if prop in MG_PROPS:
        if prop in node.attrib:
            # presentation attribute
            color = node.get(prop)
        if 'style' in node.attrib:
            # inline CSS style property
            sdict = simplestyle.parseStyle(node.get('style'))
            if prop in sdict:
                color = sdict.get(prop)
        if color.startswith('url('):
            # paint server (pattern, gradient, hatch)
            color = default
        elif color.startswith('none'):
            # no paint for prop
            color = default
    return color or default


def set_prop_color(node, prop='fill', color='#000000'):
    """Set style property *prop* of *node"."""
    prop_set = False
    if prop in MG_PROPS:
        if prop in node.attrib:
            # update presentation attribute if present
            node.set(prop, color)
            prop_set = True
        if 'style' in node.attrib or not prop_set:
            # update or add inline CSS style property
            sdict = simplestyle.parseStyle(node.get('style'))
            if prop in sdict or not prop_set:
                sdict[prop] = color
                node.set('style', simplestyle.formatStyle(sdict))


def subpath_to_meshdata(subpath):
    """Convert csp subpath to corners, edge path data."""
    if len(subpath) >= 5:
        corners = []
        edges = []
        for i, corner in enumerate(subpath[:4]):
            corners.append(corner[1])
            edge = [list(subpath[i]), list(subpath[i+1])]
            edge[0][0] = list(edge[0][1])
            edge[1][2] = list(edge[1][1])
            if is_line(edge):
                # straight line segment
                edge_data = ['L']
                edge_data.append(format_point(edge[1][1]))
            else:
                # cubic bezier curve
                edge_data = ['C']
                edge_data.append(format_point(edge[0][2]))
                edge_data.append(format_point(edge[1][0]))
                edge_data.append(format_point(edge[1][1]))
            edges.append(' '.join(edge_data))
    return corners, edges


def new_meshgradient(pos=None, rows=1, cols=1, autocollect=True):
    """Return skeleton of 1x1 meshgradient definition."""
    # initial point
    if pos is None or len(pos) != 2:
        pos = [0.0, 0.0]
    # create nested elements for rows x cols mesh
    meshgradient = inkex.etree.Element(inkex.addNS('meshgradient', 'svg'))
    for _ in range(rows):
        meshrow = inkex.etree.Element(inkex.addNS('meshrow', 'svg'))
        meshgradient.append(meshrow)
        for _ in range(cols):
            meshpatch = inkex.etree.Element(inkex.addNS('meshpatch', 'svg'))
            meshrow.append(meshpatch)
    # set meshgradient attributes
    meshgradient.set('gradientUnits', 'userSpaceOnUse')
    meshgradient.set('x', str(pos[0]))
    meshgradient.set('y', str(pos[1]))
    if autocollect:
        meshgradient.set(inkex.addNS('collect', 'inkscape'), 'always')
    return meshgradient


def meshpatch_stops(meshpatch, edges, colors):
    """Add or edit meshpatch stops with path and stop-color."""
    # iterate stops based on number of edges (path data)
    for i, edge in enumerate(edges):
        if i < len(meshpatch):
            stop = meshpatch[i]
        else:
            stop = inkex.etree.Element(inkex.addNS('stop', 'svg'))
            meshpatch.append(stop)
        # set edge path data
        stop.set('path', edge)
        # set stop color
        set_prop_color(stop, prop='stop-color', color=colors[i % 2])


def path_to_csp(node):
    """Parse path data to extract geometry for meshgradient."""
    return parsePath(node.get('d'))


def csp_to_mesh(node, csp, subpath=0):
    """Convert csp to meshgradient geometry."""
    # mesh data
    corners, edges = subpath_to_meshdata(csp[subpath])
    # alternating stop colors
    colors = [get_prop_color(node, prop='fill'), '#ffffff']
    # define meshgradient with first corner as initial point
    meshgradient = new_meshgradient(pos=corners[0], rows=1, cols=1)
    # define stops (stop-color, path) for first meshpatch
    meshpatch_stops(meshgradient[0][0], edges[0:4], colors)
    return meshgradient


def apply_mesh(node, mesh_id, prop='fill'):
    """Apply meshgradient to *node* style."""
    if mesh_id is not None:
        sdict = simplestyle.parseStyle(node.get('style'))
        sdict[prop] = 'url(#{})'.format(mesh_id)
        node.set('style', simplestyle.formatStyle(sdict))


class MeshGradients(inkex.Effect):
    """Effect-based class to process mesh gradients."""

    def __init__(self):
        """Init base clase and MeshGradients()."""
        inkex.Effect.__init__(self)

        self.OptionParser.add_option("--tab",
                                     action="store", type="string",
                                     dest="tab",
                                     help="The selected UI-tab")

    def add_mesh(self, meshgradient):
        """Add meshgradient definition to current document."""
        defs = get_defs(self.document.getroot())
        defs.append(meshgradient)
        mesh_id = self.uniqueId('meshgradient')
        meshgradient.set('id', mesh_id)
        return mesh_id


class PathToMesh(MeshGradients):
    """MeshGradients-based class to convert path data to mesh geometry."""

    def __init__(self):
        """Init base clase and PathToMesh()."""
        MeshGradients.__init__(self)

    def effect(self):
        """Main routine to convert path data to mesh geometry."""
        # loop through selection
        for node in self.selected.values():
            if is_path(node):
                csp = None
                meshgradient = None
                mesh_id = None
                # parse path data
                csp = path_to_csp(node)
                # convert csp to meshgradient definition
                if csp is not None:
                    # TODO: check length of path data / csp
                    meshgradient = csp_to_mesh(node, csp)
                # add meshgradient to document
                if meshgradient is not None:
                    mesh_id = self.add_mesh(meshgradient)
                # apply meshgradient to node
                if mesh_id is not None:
                    apply_mesh(node, mesh_id)


if __name__ == '__main__':
    ME = PathToMesh()
    ME.affect()

# vim: et shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=79
