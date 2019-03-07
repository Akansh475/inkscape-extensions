#!/usr/bin/env python
# coding=utf-8
'''
Copyright (C) 2013 Sebastian Wüst, sebi@timewaster.de

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from __future__ import print_function

# standard library
import sys
# local libraries
import hpgl_encoder
import inkex


class HpglOutput(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument('--tab')
        self.arg_parser.add_argument('--resolutionX',   type=float,         default=1016.0, help='Resolution X (dpi)')
        self.arg_parser.add_argument('--resolutionY',   type=float,         default=1016.0, help='Resolution Y (dpi)')
        self.arg_parser.add_argument('--pen',           type=int,           default=1,      help='Pen number')
        self.arg_parser.add_argument('--force',         type=int,           default=24,     help='Pen force (g)')
        self.arg_parser.add_argument('--speed',         type=int,           default=20,     help='Pen speed (cm/s)')
        self.arg_parser.add_argument('--orientation',                       default='90',   help='Rotation (Clockwise)')
        self.arg_parser.add_argument('--mirrorX',       type=inkex.inkbool, default='False',help='Mirror X axis')
        self.arg_parser.add_argument('--mirrorY',       type=inkex.inkbool, default='False',help='Mirror Y axis')
        self.arg_parser.add_argument('--center',        type=inkex.inkbool, default='False',help='Center zero point')
        self.arg_parser.add_argument('--overcut',       type=float,         default=1.0,    help='Overcut (mm)')
        self.arg_parser.add_argument('--toolOffset',    type=float,         default=0.25,   help='Tool (Knife) offset correction (mm)')
        self.arg_parser.add_argument('--precut',        type=inkex.inkbool, default=True,   help='Use precut')
        self.arg_parser.add_argument('--flat',          type=float,         default=1.2,    help='Curve flatness')
        self.arg_parser.add_argument('--autoAlign',     type=inkex.inkbool, default=True,   help='Auto align')
        self.arg_parser.add_argument('--convertObjects',type=inkex.inkbool, default=True,   help='Convert objects to paths')

    def effect(self):
        self.options.debug = False
        # get hpgl data
        myHpglEncoder = hpgl_encoder.hpglEncoder(self)
        try:
            self.hpgl, debugObject = myHpglEncoder.getHpgl()
        except Exception as inst:
            if inst.args[0] == 'NO_PATHS':
                # issue error if no paths found
                inkex.errormsg(_("No paths where found. Please convert all objects you want to save into paths."))
                self.hpgl = ''
                return
            else:
                raise
        # convert raw HPGL to HPGL
        hpglInit = 'IN'
        if self.options.force > 0:
            hpglInit += ';FS%d' % self.options.force
        if self.options.speed > 0:
            hpglInit += ';VS%d' % self.options.speed
        self.hpgl = hpglInit + self.hpgl + ';PU0,0;SP0;IN; '

    def output(self):
        # print to file
        if self.hpgl != '':
            print(self.hpgl)

if __name__ == '__main__':
    # start extension
    e = HpglOutput()
    e.affect()

