#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2006 Aaron Spike, aaron@ekips.org
# Copyright (C) 2010-2012 Nicolas Dufour, nicoduf@yahoo.fr
# (Windows support and various fixes)
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
"""
Export to Gimp's XCF file format including Grids and Guides.
"""

import os
from collections import OrderedDict

import inkex
from inkex.localization import _
from inkex.base import TempDirMixin
from inkex.command import take_snapshot, call

class GimpOutput(TempDirMixin, inkex.OutputExtension):
    """
    Provide a quick and dirty way of using gimp to output an xcf from Inkscape.

    Both Inkscape and Gimp must be installed for this extension to work.
    """
    dir_prefix = 'gimp-out-'

    def __init__(self):
        super(GimpOutput, self).__init__()
        self.arg_parser.add_argument("--tab",
                                     type=str,
                                     dest="tab")
        self.arg_parser.add_argument("-d", "--guides",
                                     type=inkex.Boolean,
                                     dest="saveGuides", default=False,
                                     help="Save the Guides with the .XCF")
        self.arg_parser.add_argument("-r", "--grid",
                                     type=inkex.Boolean,
                                     dest="saveGrid", default=False,
                                     help="Save the Grid with the .XCF")
        self.arg_parser.add_argument("-b", "--background",
                                     type=inkex.Boolean,
                                     dest="layerBackground", default=False,
                                     help="Add background color to each layer")
        self.arg_parser.add_argument("-i", "--dpi",
                                     type=float,
                                     dest="resolution", default="96",
                                     help="File resolution")

    def get_guides(self):
        """Generate a list of horzontal and vertical only guides"""
        doc_scale = self.svg.scale
        res_scale = self.options.resolution / 96.0
        page_height = self.svg.uutounit(self.svg.unittouu(self.svg.height), "px")
        page_width = self.svg.uutounit(self.svg.unittouu(self.svg.width), "px")

        horz_guides = []
        vert_guides = []
        # Grab all guide tags in the namedview tag
        for guide in self.svg.xpath("sodipodi:namedview/sodipodi:guide"):
            if guide.is_horizontal:
                # This is a horizontal guide
                pos = self.svg.uutounit(float(guide.point[1]), "px") * doc_scale
                # GIMP doesn't like guides that are outside of the image
                if 0 < pos < page_height:
                    # The origin is at the top in GIMP land
                    horz_guides.append(str(int(round(pos * res_scale))))
            elif guide.is_vertical:
                # This is a vertical guide
                pos = self.svg.uutounit(float(guide.point[0]), "px") * doc_scale
                # GIMP doesn't like guides that are outside of the image
                if 0 < pos < page_width:
                    vert_guides.append(str(int(round(pos * res_scale))))

        return ('h', ' '.join(horz_guides)), ('v', ' '.join(vert_guides))

    def get_grid(self):
        """Get the grid if asked for and return as gimpfu script"""
        scale = (self.svg.scale) * (self.options.resolution / 96.0)
        # GIMP only allows one rectangular grid
        xpath = "sodipodi:namedview/inkscape:grid[@type='xygrid' and (not(@units) or @units='px')]"
        if self.svg.xpath(xpath):
            node = self.svg.getElement(xpath)
            for attr, default, target in (('spacing', 1, 'spacing'), ('origin', 0, 'offset')):
                fmt = {'target': target}
                for dim in 'xy':
                    # These attributes could be nonexistent
                    unit = float(node.get(attr + dim, default))
                    unit = self.svg.uutounit(unit, "px") * scale
                    fmt[dim] = int(round(float(unit)))
                yield '(gimp-image-grid-set-{target} img {x} {y})'.format(**fmt)

    @property
    def docname(self):
        """Get the document name suitable for export"""
        return self.svg.get(inkex.addNS('docname', u'sodipodi')) or 'document'

    def save(self, stream):

        pngs = OrderedDict()
        valid = False

        for node in self.svg.xpath("/svg:svg/*[name()='g' or @style][@id]"):
            if not len(node): # pylint: disable=len-as-condition
                # Ignore empty layers
                continue

            valid = True
            node_id = node.get('id')
            name = node.get("inkscape:label", node_id)

            pngs[name] = take_snapshot(
                self.document,
                dirname=self.tempdir,
                name=name,
                dpi=self.options.resolution,
                export_id=node_id,
                export_id_only=True,
                export_area_page=True,
                export_background_opacity=int(bool(self.options.layerBackground))
            )

        if not valid:
            inkex.errormsg(_('This extension requires at least one non empty layer.'))
            return

        xcf = os.path.join(self.tempdir, "{}.xcf".format(self.docname))
        script_fu = """
(tracing 1)
(define
  (png-to-layer img png_filename layer_name)
  (let*
    (
      (png (car (file-png-load RUN-NONINTERACTIVE png_filename png_filename)))
      (png_layer (car (gimp-image-get-active-layer png)))
      (xcf_layer (car (gimp-layer-new-from-drawable png_layer img)))
    )
    (gimp-image-add-layer img xcf_layer -1)
    (gimp-drawable-set-name xcf_layer layer_name)
  )
)
(let*
  (
    (img (car (gimp-image-new 200 200 RGB)))
  )
  (gimp-image-set-resolution img {dpi} {dpi})
  (gimp-image-undo-disable img)
  (for-each
    (lambda (names)
      (png-to-layer img (car names) (cdr names))
    )
    (map cons '("{files}") '("{names}"))
  )

  (gimp-image-resize-to-layers img)
""".format(
    dpi=self.options.resolution,
    files='" "'.join(pngs.values()),
    names='" "'.join(list(pngs))
)

        if self.options.saveGuides:
            for dim, guides in self.get_guides():
                script_fu += """
  (for-each
    (lambda ({d}Guide)
      (gimp-image-add-{d}guide img {d}Guide)
    )
    '({g})
  )""".format(d=dim, g=guides)

        # Grid
        if self.options.saveGrid:
            for fu_let in self.get_grid():
                script_fu += "\n" + fu_let + "\n"

        script_fu += """
  (gimp-image-undo-enable img)
  (gimp-file-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) "{xcf}" "{xcf}"))
(gimp-quit 0)
            """.format(xcf=xcf)

        call('gimp', "-b", "-", i=True, batch_interpreter="plug-in-script-fu-eval", stdin=script_fu)

        with open(xcf, 'rb') as fhl:
            stream.write(fhl.read())


if __name__ == '__main__':
    GimpOutput().run()
