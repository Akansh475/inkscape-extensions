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
"""
Perspective approach & math by Dmitry Platonov, shadowjack@mail.ru, 2006
"""

import inkex
from inkex.localization import _

X, Y = range(2)

try:
    import numpy as np
    import numpy.linalg as lin
except:
    np = None


class Project(inkex.EffectExtension):
    def effect(self):
        if np is None:
            return inkex.errormsg(
                    _("Failed to import the numpy or numpy.linalg modules."
                      " These modules are required by this extension. Please install them."
                      "  On a Debian-like system this can be done with the command, "
                      "sudo apt-get install python-numpy."))
        if len(self.options.ids) < 2:
            return inkex.errormsg(_("This extension requires two selected paths."))

        # obj is selected second
        scale = self.svg.unittouu('1px')  # convert to document units
        doc = self.svg
        h = self.svg.unittouu(doc.xpath('@height')[0])
        # process viewBox height attribute to correct page scaling
        viewBox = doc.get('viewBox')
        if viewBox:
            viewBox2 = viewBox.split(',')
            if len(viewBox2) < 4:
                viewBox2 = viewBox.split(' ')
            scale *= self.svg.unittouu(self.svg.add_unit(viewBox2[3])) / h
        obj = self.svg.selected[self.options.ids[0]]
        envelope = self.svg.selected[self.options.ids[1]]
        if obj.get(inkex.addNS('type', 'sodipodi')):
            return inkex.errormsg(_("The first selected object is of type '%s'.\nTry using the procedure Path->Object to Path." % obj.get(inkex.addNS('type', 'sodipodi'))))

        if isinstance(obj, (inkex.PathElement, inkex.Group)):
            if isinstance(envelope, inkex.PathElement):
                path = envelope.path.transform(envelope.composed_transform()).to_superpath()

                if len(path) < 1 or len(path[0]) < 4:
                    return inkex.errormsg(_("This extension requires that the second selected path be four nodes long."))

                dp = np.zeros((4, 2), dtype=np.float64)
                for i in range(4):
                    dp[i][0] = path[0][i][1][0]
                    dp[i][1] = path[0][i][1][1]

                # query inkscape about the bounding box of obj
                bbox = obj.bounding_box()

                sp = np.array([
                    [bbox.left, bbox.bottom],
                    [bbox.left, bbox.top],
                    [bbox.right, bbox.top],
                    [bbox.right, bbox.bottom]], dtype=np.float64)
            else:
                if isinstance(envelope, inkex.Group):
                    return inkex.errormsg(_("The second selected object is a group, not a path.\nTry using the procedure Object->Ungroup."))
                else:
                    return inkex.errormsg(_("The second selected object is not a path.\nTry using the procedure Path->Object to Path."))
        else:
            return inkex.errormsg(_("The first selected object is not a path.\nTry using the procedure Path->Object to Path."))

        solmatrix = np.zeros((8, 8), dtype=np.float64)
        free_term = np.zeros(8, dtype=np.float64)
        for i in (0, 1, 2, 3):
            solmatrix[i][0] = sp[i][0]
            solmatrix[i][1] = sp[i][1]
            solmatrix[i][2] = 1
            solmatrix[i][6] = -dp[i][0] * sp[i][0]
            solmatrix[i][7] = -dp[i][0] * sp[i][1]
            solmatrix[i + 4][3] = sp[i][0]
            solmatrix[i + 4][4] = sp[i][1]
            solmatrix[i + 4][5] = 1
            solmatrix[i + 4][6] = -dp[i][1] * sp[i][0]
            solmatrix[i + 4][7] = -dp[i][1] * sp[i][1]
            free_term[i] = dp[i][0]
            free_term[i + 4] = dp[i][1]

        res = lin.solve(solmatrix, free_term)
        projmatrix = np.array([[res[0], res[1], res[2]], [res[3], res[4], res[5]], [res[6], res[7], 1.0]], dtype=np.float64)
        if obj.tag == inkex.addNS("path", 'svg'):
            self.process_path(obj, projmatrix)
        if obj.tag == inkex.addNS("g", 'svg'):
            self.process_group(obj, projmatrix)

    def process_group(self, group, matrix):
        for node in group:
            if node.tag == inkex.addNS('path', 'svg'):
                self.process_path(node, matrix)
            if node.tag == inkex.addNS('g', 'svg'):
                self.process_group(node, matrix)

    def process_path(self, element, matrix):
        mat = element.composed_transform()
        point = element.path.transform(mat).to_superpath()
        for subs in point:
            for csp in subs:
                csp[0] = self.project_point(csp[0], matrix)
                csp[1] = self.project_point(csp[1], matrix)
                csp[2] = self.project_point(csp[2], matrix)
        element.path = inkex.Path(point).transform(-mat)

    def project_point(self, point, matrix):
        return [(point[X] * matrix[0][0] + point[Y] * matrix[0][1] + matrix[0][2]) /
                (point[X] * matrix[2][0] + point[Y] * matrix[2][1] + matrix[2][2]),
                (point[X] * matrix[1][0] + point[Y] * matrix[1][1] + matrix[1][2]) /
                (point[X] * matrix[2][0] + point[Y] * matrix[2][1] + matrix[2][2])]


if __name__ == '__main__':
    Project().run()
