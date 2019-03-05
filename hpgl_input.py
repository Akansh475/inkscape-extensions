#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2013 Sebastian Wüst, sebi@timewaster.de
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

import sys

import hpgl_decoder
import inkex
import inkex.base
from inkex.localize import _

class HpglFile(inkex.base.SvgOutputMixin, inkex.base.InkscapeExtension):
    def __init__(self):
        super(HpglFile, self).__init__()
        self.arg_parser.add_argument('--resolutionX', type=float, default=1016.0, help='Resolution X (dpi)')
        self.arg_parser.add_argument('--resolutionY', type=float, default=1016.0, help='Resolution Y (dpi)')
        self.arg_parser.add_argument('--showMovements', type=inkex.inkbool, default=False, help='Show Movements between paths')
        self.arg_parser.add_argument('--docWidth', type=float, default=210.0, help='Width in mm')
        self.arg_parser.add_argument('--docHeight', type=float, default=297.0, help='Height in mm')

    def load(self, stream):
        return ';'.join(line.strip() for line in stream)

    def effect(self):
        # interpret HPGL data
        myHpglDecoder = hpgl_decoder.hpglDecoder(self.document, self.options)
        self.document = None

        try:
            doc, warnings = myHpglDecoder.getSvg()
        except Exception as inst:
            if inst.args[0] == 'NO_HPGL_DATA':
                # issue error if no hpgl data found
                inkex.errormsg(_("No HPGL data found."))
                exit(1)
            else:
                type, value, traceback = sys.exc_info()
                raise ValueError("", type, value).with_traceback(traceback)

        # issue warning if unknown commands where found
        if 'UNKNOWN_COMMANDS' in warnings:
            inkex.errormsg(_("The HPGL data contained unknown (unsupported) commands, there is a possibility that the drawing is missing some content."))

        # deliver document to inkscape
        self.document = doc

if __name__ == '__main__':
    HpglFile().run()

