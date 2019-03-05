#!/usr/bin/env python 
#
# Copyright (C) 2015 ~suv <suv-sf@users.sf.net>
# Copyright (C) 2010 Alvin Penner
# Copyright (C) 2006 Georg Wiora
# Copyright (C) 2006 Nathan Hurst
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
#TODO:
# * should use the standard attributes for text
# * Implement option to keep text orientation upright 
#    1. Find text direction i.e. path tangent,
#    2. check direction >90 or <-90 Degrees
#    3. rotate by 180 degrees around text center
#
"""
This extension module can measure arbitrary path and object length
It adds text to the selected path containing the length in a given unit.
Area and Center of Mass calculated using Green's Theorem:
http://mathworld.wolfram.com/GreensTheorem.html
"""

import re
import locale

import inkex
from inkex import inkbool


# On darwin, fall back to C in cases of 
# - incorrect locale IDs (see comments in bug #406662)
# - https://bugs.python.org/issue18378
try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'C')

# third party
try:
    import numpy
    mat_area   = numpy.matrix([[  0,  2,  1, -3],[ -2,  0,  1,  1],[ -1, -1,  0,  2],[  3, -1, -2,  0]])
    mat_cofm_0 = numpy.matrix([[  0, 35, 10,-45],[-35,  0, 12, 23],[-10,-12,  0, 22],[ 45,-23,-22,  0]])
    mat_cofm_1 = numpy.matrix([[  0, 15,  3,-18],[-15,  0,  9,  6],[ -3, -9,  0, 12],[ 18, -6,-12,  0]])
    mat_cofm_2 = numpy.matrix([[  0, 12,  6,-18],[-12,  0,  9,  3],[ -6, -9,  0, 15],[ 18, -3,-15,  0]])
    mat_cofm_3 = numpy.matrix([[  0, 22, 23,-45],[-22,  0, 12, 10],[-23,-12,  0, 35],[ 45,-10,-35,  0]])
except:
    numpy = None


class Length(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--type",
                        action="store", type=str,
                        dest="mtype", default="length",
                        help="Type of measurement")
        self.arg_parser.add_argument("--format",
                        action="store", type=str,
                        dest="mformat", default="textonpath",
                        help="Text Orientation")
        self.arg_parser.add_argument("--presetFormat",
                        action="store", type=str,
                        dest="presetFormat", default="TaP_start",
                        help="Preset text layout")
        self.arg_parser.add_argument("--startOffset",
                        action="store", type=str,
                        dest="startOffset", default="custom",
                        help="Text Offset along Path")
        self.arg_parser.add_argument("--startOffsetCustom",
                        action="store", type=int,
                        dest="startOffsetCustom", default=50,
                        help="Text Offset along Path")
        self.arg_parser.add_argument("--anchor",
                        action="store", type=str,
                        dest="anchor", default="start",
                        help="Text Anchor")
        self.arg_parser.add_argument("--position",
                        action="store", type=str,
                        dest="position", default="start",
                        help="Text Position")
        self.arg_parser.add_argument("--angle",
                        action="store", type=float,
                        dest="angle", default=0,
                        help="Angle")
        self.arg_parser.add_argument("-f", "--fontsize",
                        action="store", type=int,
                        dest="fontsize", default=20,
                        help="Size of length label text in px")
        self.arg_parser.add_argument("-o", "--offset",
                        action="store", type=float,
                        dest="offset", default=-6,
                        help="The distance above the curve")
        self.arg_parser.add_argument("-u", "--unit",
                        action="store", type=str,
                        dest="unit", default="mm",
                        help="The unit of the measurement")
        self.arg_parser.add_argument("-p", "--precision",
                        action="store", type=int,
                        dest="precision", default=2,
                        help="Number of significant digits after decimal point")
        self.arg_parser.add_argument("-s", "--scale",
                        action="store", type=float,
                        dest="scale", default=1,
                        help="Scale Factor (Drawing:Real Length)")
        self.arg_parser.add_argument("-r", "--orient",
                        action="store", type=inkbool,
                        dest="orient", default=True,
                        help="Keep orientation of text upright")
        self.arg_parser.add_argument("--tab",
                        action="store", type=str,
                        dest="tab", default="sampling",
                        help="The selected UI-tab when OK was pressed") 
        self.arg_parser.add_argument("--measurehelp",
                        action="store", type=str,
                        dest="measurehelp", default="",
                        help="dummy")

    def effect(self):
        if numpy is None:
            inkex.errormsg(_("Failed to import the numpy modules. These modules are required by this extension. Please install them and try again.  On a Debian-like system this can be done with the command, sudo apt-get install python-numpy."))
            return

        if self.options.mformat == '"presets"':
            self.setPreset()
        # get number of digits
        prec = int(self.options.precision)
        scale = self.unittouu('1px')    # convert to document units
        self.options.offset *= scale
        factor = 1.0
        doc = self.document.getroot()
        if doc.get('viewBox'):
            (viewx, viewy, vieww, viewh) = re.sub(' +|, +|,',' ',doc.get('viewBox')).strip().split(' ', 4)
            factor = self.unittouu(doc.get('width'))/float(vieww)
            if self.unittouu(doc.get('height'))/float(viewh) < factor:
                factor = self.unittouu(doc.get('height'))/float(viewh)
            factor /= self.unittouu('1px')
            self.options.fontsize /= factor
        factor *= scale/self.unittouu('1'+self.options.unit)
        # loop over all selected paths
        for id, node in self.selected.items():
            if node.tag == inkex.addNS('path','svg'):
                mat = inkex.composeParents(node, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
                p = inkex.parseCubicPath(node.get('d'))
                inkex.applyTransformToPath(mat, p)
                if self.options.mtype == "length":
                    slengths, stotal = csplength(p)
                    self.group = inkex.etree.SubElement(node.getparent(),inkex.addNS('text','svg'))
                elif self.options.mtype == "area":
                    stotal = abs(csparea(p)*factor*self.options.scale)
                    self.group = inkex.etree.SubElement(node.getparent(),inkex.addNS('text','svg'))
                else:
                    xc, yc = cspcofm(p)
                    self.group = inkex.etree.SubElement(node.getparent(),inkex.addNS('path','svg'))
                    self.group.set('id', 'MassCenter_' + node.get('id'))
                    self.addCross(self.group, xc, yc, scale)
                    continue
                # Format the length as string
                lenstr = locale.format("%(len)25."+str(prec)+"f",{'len':round(stotal*factor*self.options.scale,prec)}).strip()
                if self.options.mformat == '"textonpath"':
                    startOffset = self.options.startOffset
                    if startOffset == "custom":
                        startOffset = str(self.options.startOffsetCustom) + '%'
                    if self.options.mtype == "length":
                        self.addTextOnPath(self.group, 0, 0, lenstr+' '+self.options.unit, id, self.options.anchor, startOffset, self.options.offset)
                    else:
                        self.addTextOnPath(self.group, 0, 0, lenstr+' '+self.options.unit+'^2', id, self.options.anchor, startOffset, self.options.offset)
                elif self.options.mformat == '"fixedtext"':
                    if self.options.position == "mass":
                        tx, ty = cspcofm(p)
                        anchor = 'middle'
                    elif self.options.position == "center":
                        bbox = inkex.computeBBox([node])
                        tx = bbox[0] + (bbox[1] - bbox[0])/2.0
                        ty = bbox[2] + (bbox[3] - bbox[2])/2.0
                        anchor = 'middle'
                    else:  # default
                        tx = p[0][0][1][0]
                        ty = p[0][0][1][1]
                        anchor = 'start'
                    if self.options.mtype == "length":
                        self.addTextWithTspan(self.group, tx, ty, lenstr+' '+self.options.unit, id, anchor, -int(self.options.angle), self.options.offset + self.options.fontsize/2)
                    else:
                        self.addTextWithTspan(self.group, tx, ty, lenstr+' '+self.options.unit+'^2', id, anchor, -int(self.options.angle), -self.options.offset + self.options.fontsize/2)
                else:
                    # center of mass, no text
                    pass

    def setPreset(self):
        # keep dict in sync with enum in INX file:
        preset_dict = {
            'default_length': ['"textonpath"', "50%", "start", None, None],
            'default_area': ['"fixedtext"', None, None, "start", 0.0],
            'default_cofm': [None, None, None, None, None],
            'TaP_start': ['"textonpath"', "0%", "start", None, None],
            'TaP_middle': ['"textonpath"', "50%", "middle", None, None],
            'TaP_end': ['"textonpath"', "100%", "end", None, None],
            'FT_start': ['"fixedtext"', None, None, "start", 0.0],
            'FT_bbox': ['"fixedtext"', None, None, "center", 0.0],
            'FT_mass': ['"fixedtext"', None, None, "mass", 0.0],
        }
        if self.options.presetFormat == "default":
            current_preset = 'default_' + self.options.mtype
        else:
            current_preset = self.options.presetFormat
        self.options.mformat = preset_dict[current_preset][0]
        self.options.startOffset = preset_dict[current_preset][1]
        self.options.anchor = preset_dict[current_preset][2]
        self.options.position = preset_dict[current_preset][3]
        self.options.angle = preset_dict[current_preset][4]

    def addCross(self, node, x, y, scale):
        l = 3*scale         # 3 pixels in document units
        node.set('d', 'm %s,%s %s,0 %s,0 m %s,%s 0,%s 0,%s' % (str(x-l), str(y), str(l), str(l), str(-l), str(-l), str(l), str(l)))
        node.set('style', 'stroke:#000000;fill:none;stroke-width:%s' % str(0.5*scale))

    def addTextOnPath(self, node, x, y, text, id, anchor, startOffset, dy = 0):
                new = inkex.etree.SubElement(node,inkex.addNS('textPath','svg'))
                s = {'text-align': 'center', 'vertical-align': 'bottom',
                    'text-anchor': anchor, 'font-size': str(self.options.fontsize),
                    'fill-opacity': '1.0', 'stroke': 'none',
                    'font-weight': 'normal', 'font-style': 'normal', 'fill': '#000000'}
                new.set('style', str(inkex.Style(s)))
                new.set(inkex.addNS('href','xlink'), '#'+id)
                new.set('startOffset', startOffset)
                new.set('dy', str(dy)) # dubious merit
                #new.append(tp)
                if text[-2:] == "^2":
                    appendSuperScript(new, "2")
                    new.text = str(text)[:-2]
                else:
                    new.text = str(text)
                #node.set('transform','rotate(180,'+str(-x)+','+str(-y)+')')
                node.set('x', str(x))
                node.set('y', str(y))

    def addTextWithTspan(self, node, x, y, text, id, anchor, angle, dy = 0):
                new = inkex.etree.SubElement(node,inkex.addNS('tspan','svg'), {inkex.addNS('role','sodipodi'): 'line'})
                s = {'text-align': 'center', 'vertical-align': 'bottom',
                    'text-anchor': anchor, 'font-size': str(self.options.fontsize),
                    'fill-opacity': '1.0', 'stroke': 'none',
                    'font-weight': 'normal', 'font-style': 'normal', 'fill': '#000000'}
                new.set('style', str(inkex.Style(s)))
                new.set('dy', str(dy))
                if text[-2:] == "^2":
                    appendSuperScript(new, "2")
                    new.text = str(text)[:-2]
                else:
                    new.text = str(text)
                node.set('x', str(x))
                node.set('y', str(y))
                node.set('transform', 'rotate(%s, %s, %s)' % (angle, x, y))

if __name__ == '__main__':
    e = Length()
    e.affect()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
