#!/usr/bin/env python
#
# Copyright (C) 2007 Martin Owens
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110, USA.
#
"""
Inkscape's general barcode extension. Run from within inkscape or use the
Barcode module provided for outside or scripting.
"""

import sys
import inkex

from barcode import get_barcode

class InsertBarcode(inkex.Effect):
    """
    Raw barcode Effect class, see Barcode base class.
    """
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option(
            "-l", "--height", action="store", type="int",
            dest="height", default=30, help="Barcode Height")
        self.OptionParser.add_option(
            "-t", "--type", action="store", type="string",
            dest="type", default='', help="Barcode Type")
        self.OptionParser.add_option(
            "-d", "--text", action="store", type="string",
            dest="text", default='', help="Text to print on barcode")

    def effect(self):
        (pos_x, pos_y) = inkex.computePointInNode(
            list(self.view_center), self.current_layer)

        barcode = get_barcode(
            self.options.type,
            text=self.options.text,
            height=self.options.height,
            document=self.document,
            x=pos_x, y=pos_y,
            scale=self.unittouu('1px'),
        ).generate()
        if barcode is not None:
            self.current_layer.append(barcode)
        else:
            sys.stderr.write("No barcode was generated\n")

if __name__ == '__main__':
    InsertBarcode().affect()

