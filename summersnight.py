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

import inkex
from inkex.localize import _
from inkex.paths import Path
from inkex.transforms import Segment
from inkex.generic import EffectExtension
from inkex.elements import PathElement, Group
from inkex.cubic_paths import CubicSuperPath, unCubicSuperPath

class Project(EffectExtension):
    def effect(self):
        if len(self.options.ids) < 2:
            inkex.errormsg(_("This extension requires two selected paths. \nThe second path must be exactly four nodes long."))
            return

        #obj is selected second
        scale = self.svg.unittouu('1px')    # convert to document units
        doc = self.document.getroot()
        h = self.svg.unittouu(doc.xpath('@height', namespaces=inkex.NSS)[0])
        # process viewBox height attribute to correct page scaling
        viewBox = doc.get('viewBox')
        if viewBox:
            viewBox2 = viewBox.split(',')
            if len(viewBox2) < 4:
                viewBox2 = viewBox.split(' ')
            scale *= self.svg.unittouu(self.svg.add_unit(viewBox2[3])) / h

        obj = self.svg.selected[self.options.ids[0]]
        trafo = self.svg.selected[self.options.ids[1]]

        if obj.get(inkex.addNS('type','sodipodi')):
            return inkex.errormsg(_("The first selected object is of type '%s'.\nTry using the procedure Path->Object to Path." % obj.get(inkex.addNS('type','sodipodi'))))
        if isinstance(obj, (PathElement, Group)):
            if isinstance(trafo, PathElement):
                # distil trafo into four node points
                trafo.apply_transform()
                trafo = CubicSuperPath(trafo.path.to_arrays())
                if len(trafo[0]) < 4:
                    return inkex.errormsg(_("This extension requires that the second selected path be four nodes long."))
                trafo = [[(csp[1][0], csp[1][1]) for csp in subs] for subs in trafo][0][:4]

                #vectors pointing away from the trafo origin
                self.t1 = Segment((trafo[0], trafo[1]))
                self.t2 = Segment((trafo[1], trafo[2]))
                self.t3 = Segment((trafo[3], trafo[2]))
                self.t4 = Segment((trafo[0], trafo[3]))
                self.bbox = obj.bounding_box()

                self.process_group([obj])
            else:
                if isinstance(trafo, Group):
                    inkex.errormsg(_("The second selected object is a group, not a path.\nTry using the procedure Object->Ungroup."))
                else:
                    inkex.errormsg(_("The second selected object is not a path.\nTry using the procedure Path->Object to Path."))
        else:
            inkex.errormsg(_("The first selected object is not a path.\nTry using the procedure Path->Object to Path."))

    def process_group(self, group):
        for node in group:
            if isinstance(node, PathElement):
                self.process_path(node)
            elif isinstance(node, Group):
                self.process_group(node)

    def process_path(self, node):
        node.apply_transform()
        points = CubicSuperPath(node.path.to_arrays())
        #simpletransform.applyTransformToPath(mat, p)
        for subs in points:
            for csp in subs:
                csp[0] = self.trafopoint(csp[0])
                csp[1] = self.trafopoint(csp[1])
                csp[2] = self.trafopoint(csp[2])

        node.path = Path(unCubicSuperPath(points))

    def trafopoint(self, xy):
        """Transform algorithm thanks to Jose Hevia (freon)"""
        (x, y) = xy
        vector = Segment(((self.bbox.left, self.bbox.top), (x, y)))
        xratio = vector.width / self.bbox.width
        yratio = vector.height / self.bbox.height
        horz = Segment((self.t1.point_at_ratio(xratio), self.t3.point_at_ratio(xratio)))
        vert = Segment((self.t4.point_at_ratio(yratio), self.t2.point_at_ratio(yratio)))
        return vert.intersect(horz)


if __name__ == '__main__':
    Project().run()


