#!/bin/env python3
# coding=utf-8
#
# Copyright (C) 2019 Marc Jeanmougin, Cédric Gémy, a-l-e
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
#


import os
import sys
from subprocess import call
import inkex
from inkex.base import TempDirMixin
from inkex.command import take_snapshot, call


scribus_exe = "scribus"


# several things could be taken into consideration here :
# - the fact that openDoc works on svg files is a workaround
# - the commented parts should be the correct way to do things
#   and even include a possibility to add margins
#   BUT currently fails to place the SVG document
#   (object placed top-left instead of SVG placed top-left)
class Scribus(TempDirMixin, inkex.OutputExtension):
    def generate_script(self, stream, width, height):
        margin = 0
        stream.write(r"""
import scribus
import sys
class exportPDF():
    def __init__(self, svg=sys.argv[1], o=sys.argv[2]):
        #scribus.newDocument((%d,%d), (%d,%d,%d,%d), PORTRAIT, 1, UNIT_MILLIMETERS, PAGE_1, 0, 1)
        #scribus.placeSVG(svg, 0, 0)
        scribus.openDoc(svg)
        pdf = scribus.PDFfile()
        pdf.file = o
        pdf.save()
exportPDF()
""" % (width, height, margin, margin, margin, margin) )
        
    def save(self, stream):
        input_file = self.options.input_file
        py_file = os.path.join(self.tempdir, 'scribus.py')
        svg_file = os.path.join(self.tempdir, 'in.svg')

        with open(input_file) as f:
            with open(svg_file, "w") as f1:
                for line in f:
                    f1.write(line)
            f.close()
        
        pdf_file = os.path.join(self.tempdir, 'out.pdf')
        width = self.svg.unittouu(self.svg.get('width'))
        height = self.svg.unittouu(self.svg.get('height'))
        
        with open(py_file, 'w') as fhl:
            self.generate_script(fhl, width, height)
        call(scribus_exe, '-g', '-py', py_file, svg_file, pdf_file)
        with open(pdf_file, 'rb') as fhl:
            stream.write(fhl.read())


if __name__ == '__main__':
    Scribus().run()

