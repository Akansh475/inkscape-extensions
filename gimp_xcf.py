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

import os
import re
import shutil
import sys
import tempfile

import inkex
from inkex import inkbool


# Define extension exceptions
class GimpXCFError(Exception):
    pass


class GimpXCFExpectedIOError(GimpXCFError):
    pass


class GimpXCFInkscapeNotInstalled(GimpXCFError):
    def __init__(self):
        inkex.errormsg(_('Inkscape must be installed and set in your path variable.'))


class GimpXCFGimpNotInstalled(GimpXCFError):
    def __init__(self):
        inkex.errormsg(_('Gimp must be installed and set in your path variable.'))


class GimpXCFScriptFuError(GimpXCFError):
    def __init__(self):
        inkex.errormsg(_('An error occurred while processing the XCF file.'))


class MyEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--tab",
                                     type=str,
                                     dest="tab")
        self.arg_parser.add_argument("-d", "--guides",
                                     type=inkbool,
                                     dest="saveGuides", default=False,
                                     help="Save the Guides with the .XCF")
        self.arg_parser.add_argument("-r", "--grid",
                                     type=inkbool,
                                     dest="saveGrid", default=False,
                                     help="Save the Grid with the .XCF")
        self.arg_parser.add_argument("-b", "--background",
                                     type=inkbool,
                                     dest="layerBackground", default=False,
                                     help="Add background color to each layer")
        self.arg_parser.add_argument("-i", "--dpi",
                                     type=str,
                                     dest="resolution", default="96",
                                     help="File resolution")

    def output(self):
        pass

    def clear_tmp(self):
        shutil.rmtree(self.tmp_dir)

    def getDocumentScale(self):
        """Returns the ratio between the SVG width and viewBox attributes.
        """
        documentscale = 1  # default to 1
        svgwidth = self.svg.width
        viewboxstr = self.document.getroot().get('viewBox')
        if viewboxstr:
            param = re.compile(r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)')
            p = param.match(svgwidth)
            width = 100  # default
            viewboxwidth = 100  # default
            if p:
                width = float(p.string[p.start():p.end()])
            else:
                inkex.errormsg("SVG Width not set correctly! Assuming width = 100")

            viewboxnumbers = []
            for t in viewboxstr.split():
                try:
                    viewboxnumbers.append(float(t))
                except ValueError:
                    pass
            if len(viewboxnumbers) == 4:  # check for correct number of numbers
                viewboxwidth = viewboxnumbers[2]

            documentscale = self.svg.unittouu(str(width / viewboxwidth))

        return documentscale

    def effect(self):
        svg_file = self.svg
        ttmp_orig = self.document.getroot()
        docname = ttmp_orig.get(inkex.addNS('docname', u'sodipodi'))
        if docname is None:
            docname = self.svg

        doc_scale = self.getDocumentScale()
        res_scale = eval(self.options.resolution) / 96.0
        scale = doc_scale * res_scale

        pageHeight = self.svg.uutounit(self.svg.unittouu(self.svg.width), "px")
        pageWidth = self.svg.uutounit(self.svg.unittouu(self.svg.width), "px")

        # Create os temp dir (to store exported pngs and Gimp log file)
        self.tmp_dir = tempfile.mkdtemp()

        # Guides
        hGuides = []
        vGuides = []
        if self.options.saveGuides:
            # Grab all guide tags in the namedview tag
            guideXpath = "sodipodi:namedview/sodipodi:guide"
            for guideNode in self.document.xpath(guideXpath, namespaces=inkex.NSS):
                ori = guideNode.get('orientation')
                if ori == '0,1':
                    # This is a horizontal guide
                    pos = self.uutounit(float(guideNode.get('position').split(',')[1]), "px") * doc_scale
                    # GIMP doesn't like guides that are outside of the image
                    if 0 < pos < pageHeight:
                        # The origin is at the top in GIMP land
                        hGuides.append(str(int(round((pageHeight - pos) * res_scale))))
                elif ori == '1,0':
                    # This is a vertical guide
                    pos = self.uutounit(float(guideNode.get('position').split(',')[0]), "px") * doc_scale
                    # GIMP doesn't like guides that are outside of the image
                    if 0 < pos < pageWidth:
                        vGuides.append(str(int(round(pos * res_scale))))

        hGList = ' '.join(hGuides)
        vGList = ' '.join(vGuides)

        # Grid
        gridSpacingFunc = ''
        gridOriginFunc = ''
        # GIMP only allows one rectangular grid
        gridXpath = "sodipodi:namedview/inkscape:grid[@type='xygrid' and (not(@units) or @units='px')]"
        if self.options.saveGrid and self.document.xpath(gridXpath, namespaces=inkex.NSS):
            gridNode = self.xpathSingle(gridXpath)
            if gridNode is not None:
                # These attributes could be nonexistent
                spacingX = gridNode.get('spacingx')
                if spacingX is None:
                    spacingX = 1
                else:
                    spacingX = self.uutounit(float(spacingX), "px") * scale
                spacingY = gridNode.get('spacingy')
                if spacingY is None:
                    spacingY = 1
                else:
                    spacingY = self.uutounit(float(spacingY), "px") * scale
                originX = gridNode.get('originx')
                if originX is None:
                    originX = 0
                else:
                    originX = self.uutounit(float(originX), "px") * scale
                originY = gridNode.get('originy')
                if originY is None:
                    originY = 0
                else:
                    originY = self.uutounit(float(originY), "px") * doc_scale
                    offsetY = pageHeight % (self.uutounit(float(spacingY), "px") * doc_scale)
                    originY = (pageHeight - originY) * res_scale

                gridSpacingFunc = '(gimp-image-grid-set-spacing img {} {})'.format(int(round(float(spacingX))), int(round(float(spacingY))))
                gridOriginFunc = '(gimp-image-grid-set-offset img {} {})'.format(int(round(float(originX))), int(round(float(originY))))

        # Layers
        area = '--export-area-page'
        opacity = '--export-background-opacity='
        resolution = '--export-dpi=' + self.options.resolution

        if self.options.layerBackground:
            opacity += "1"
        else:
            opacity += "0"
        pngs = []
        names = []
        self.valid = 0
        path = "/svg:svg/*[name()='g' or @style][@id]"
        for node in self.document.xpath(path, namespaces=inkex.NSS):
            if len(node) > 0:  # Get rid of empty layers
                self.valid = 1
                id = node.get('id')
                if node.get("{" + inkex.NSS["inkscape"] + "}label"):
                    name = node.get("{" + inkex.NSS["inkscape"] + "}label")
                else:
                    name = id
                filename = os.path.join(self.tmp_dir, "{}.png".format(id))
                command = "inkscape -i \"{}\" -j {} {} -e \"{}\" {} {}".format(id, area, opacity, filename, svg_file, resolution)

                # XXX This must be replaced!
                # p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                # return_code = p.wait()
                # f = p.stdout
                # err = p.stderr
                # stdin = p.stdin
                # f.read()
                # f.close()
                # err.close()
                # stdin.close()

                if os.name == 'nt':
                    filename = filename.replace("\\", "/")
                pngs.append(filename)
                names.append(name)

        if self.valid == 0:
            self.clear_tmp()
            inkex.errormsg(_('This extension requires at least one non empty layer.'))
        else:
            filelist = '"{}"'.format('" "'.join(pngs))
            namelist = '"{}"'.format('" "'.join(names))
            xcf = os.path.join(self.tmp_dir, "{}.xcf".format(docname))
            if os.name == 'nt':
                xcf = xcf.replace("\\", "/")
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
  (gimp-image-set-resolution img {} {})
  (gimp-image-undo-disable img)
  (for-each
    (lambda (names)
      (png-to-layer img (car names) (cdr names))
    )
    (map cons '({}) '({}))
  )

  (gimp-image-resize-to-layers img)

  (for-each
    (lambda (hGuide)
      (gimp-image-add-hguide img hGuide)
    )
    '({})
  )

  (for-each
    (lambda (vGuide)
      (gimp-image-add-vguide img vGuide)
    )
    '({})
  )

  {}
  {}

  (gimp-image-undo-enable img)
  (gimp-file-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) "{}" "{}"))
(gimp-quit 0)
            """.format(self.options.resolution, self.options.resolution, filelist, namelist, hGList, vGList, gridSpacingFunc, gridOriginFunc, xcf, xcf)

            junk = os.path.join(self.tmp_dir, 'junk_from_gimp.txt')
            command = 'gimp -i --batch-interpreter plug-in-script-fu-eval -b - > {} 2>&1'.format(junk)

            # p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            # f = p.stdin
            # out = p.stdout
            # err = p.stderr
            # f.write(script_fu.encode('utf-8'))
            # return_code = p.wait()

            # f.close()
            # err.close()
            # out.close()
            # Uncomment these lines to see the output from gimp
            # err = open(junk, 'r')
            # inkex.debug(err.read())
            # err.close()

            try:
                x = open(xcf, 'rb')
            except:
                self.clear_tmp()
                raise GimpXCFScriptFuError

            if os.name == 'nt':
                try:
                    import msvcrt
                    msvcrt.setmode(1, os.O_BINARY)
                except:
                    pass
            try:
                stdout = sys.stdout if sys.version_info[0] < 3 else sys.stdout.buffer
                stdout.write(x.read())
            finally:
                x.close()
                self.clear_tmp()


if __name__ == '__main__':
    MyEffect().run()
