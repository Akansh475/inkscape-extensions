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

import inkex
from inkex.localization import _

import hpgl_encoder

class Plot(inkex.EffectExtension):
    """Generate a plot in HPGL output"""
    def add_arguments(self, pars):
        pars.add_argument('--tab')
        pars.add_argument('--portType', default='serial', help='Port type')
        pars.add_argument('--parallelPort', default='/dev/usb/lp2', help='Parallel port')
        pars.add_argument('--serialPort', default='COM1', help='Serial port')
        pars.add_argument('--serialBaudRate', default='9600', help='Serial Baud rate')
        pars.add_argument('--serialByteSize', default='eight', help='Serial byte size')
        pars.add_argument('--serialStopBits', default='one', help='Serial stop bits')
        pars.add_argument('--serialParity', default='none', help='Serial parity')
        pars.add_argument('--serialFlowControl', default='0', help='Flow control')
        pars.add_argument('--commandLanguage', default='hpgl', help='Command Language')
        pars.add_argument('--resolutionX', type=float, default=1016.0, help='Resolution X (dpi)')
        pars.add_argument('--resolutionY', type=float, default=1016.0, help='Resolution Y (dpi)')
        pars.add_argument('--pen', type=int, default=1, help='Pen number')
        pars.add_argument('--force', type=int, default=24, help='Pen force (g)')
        pars.add_argument('--speed', type=int, default=20, help='Pen speed (cm/s)')
        pars.add_argument('--orientation', default='90', help='Rotation (Clockwise)')
        pars.add_argument('--mirrorX', type=inkex.inkbool, default=False, help='Mirror X axis')
        pars.add_argument('--mirrorY', type=inkex.inkbool, default=False, help='Mirror Y axis')
        pars.add_argument('--center', type=inkex.inkbool, default=False, help='Center zero point')
        pars.add_argument('--overcut', type=float, default=1.0, help='Overcut (mm)')
        pars.add_argument('--precut', type=inkex.inkbool, default=True, help='Use precut')
        pars.add_argument('--flat', type=float, default=1.2, help='Curve flatness')
        pars.add_argument('--autoAlign', type=inkex.inkbool, default=True, help='Auto align')
        pars.add_argument('--toolOffset', type=float, default=0.25,\
            help='Tool (Knife) offset correction (mm)')
        pars.add_argument('--convertObjects', type=inkex.inkbool, default=True,\
            help='Convert objects to paths')

    def effect(self):
        # get hpgl data
        encoder = hpgl_encoder.hpglEncoder(self)
        try:
            self.hpgl = encoder.getHpgl()
        except hpgl_encoder.NoPathError:
            inkex.errormsg(_("No paths where found. Please convert objects into paths."))
            return

        # TODO: Get preview to work. This requires some work on the C++ side to be able to determine if it is
        # a preview or a final run. (Remember to set <effect needs-live-preview='false'> to true)
        '''
        if MAGIC:
            # reparse data for preview
            self.options.showMovements = True
            self.options.docWidth = self.svg.uutounit(self.unittouu(self.document.getroot().get('width')), "px")
            self.options.docHeight = self.svg.uutounit(self.unittouu(self.document.getroot().get('height')), "px")
            myHpglDecoder = hpgl_decoder.hpglDecoder(self.hpgl, self.options)
            doc, warnings = myHpglDecoder.getSvg()
            # deliver document to inkscape
            self.document = doc
        else:
        '''
        # convert to other formats
        if self.options.commandLanguage == 'HPGL':
            self.convertToHpgl()
        if self.options.commandLanguage == 'DMPL':
            self.convertToDmpl()
        if self.options.commandLanguage == 'KNK':
            self.convertToKNK()
        # output
        if self.options.portType == 'parallel':
            self.sendHpglToParallel()
        elif self.options.portType == 'serial':
            self.sendHpglToSerial()

    def convertToHpgl(self):
        # convert raw HPGL to HPGL
        hpgl_init = 'IN'
        if self.options.force > 0:
            hpgl_init += ';FS%d' % self.options.force
        if self.options.speed > 0:
            hpgl_init += ';VS%d' % self.options.speed
        self.hpgl = hpgl_init + self.hpgl + ';SP0;PU0,0;IN; '

    def convertToDmpl(self):
        # convert HPGL to DMPL
        # ;: = Initialise plotter
        # H = Home position
        # A = Absolute pen positioning
        # Ln = Line type
        # Pn = Pen select
        # Vn = velocity
        # ECn = Coordinate addressing, 1: 0.001 inch, 5: 0.005 inch, M: 0.1 mm
        # D = Pen down
        # U = Pen up
        # Z = Reset plotter
        # n,n, = Coordinate pair
        self.hpgl = self.hpgl.replace(';', ',')
        self.hpgl = self.hpgl.replace('SP', 'P')
        self.hpgl = self.hpgl.replace('PU', 'U')
        self.hpgl = self.hpgl.replace('PD', 'D')
        dmplInit = ';:HAL0'
        if self.options.speed > 0:
            dmplInit += 'V%d' % self.options.speed
        dmplInit += 'EC1'
        self.hpgl = dmplInit + self.hpgl[1:] + ',P0,U0,0,Z '

    def convertToKNK(self):
        # convert HPGL to KNK Plotter Language
        hpgl_init = 'ZG'
        if self.options.force > 0:
            hpgl_init += ';FS%d' % self.options.force
        if self.options.speed > 0:
            hpgl_init += ';VS%d' % self.options.speed
        self.hpgl = hpgl_init + self.hpgl + ';SP0;PU0,0;@ '

    def sendHpglToParallel(self):
        port = open(self.options.parallelPort, "w")
        port.write(self.hpgl)
        port.close()

    def sendHpglToSerial(self):
        # gracefully exit script when pySerial is missing
        try:
            import serial
        except ImportError as e:
            inkex.errormsg(_("pySerial is not installed. Please follow these steps:")
                + "\n\n" + _("1. Download and extract (unzip) this file to your local harddisk:")
                + "\n"   +   "   https://pypi.python.org/packages/source/p/pyserial/pyserial-2.7.tar.gz"
                + "\n"   + _("2. Copy the \"serial\" folder (Can be found inside the just extracted folder)")
                + "\n"   + _("   into the following Inkscape folder: C:\\[Program files]\\inkscape\\python\\Lib\\")
                + "\n"   + _("3. Close and restart Inkscape."))
            return
        # init serial framework
        comx = serial.Serial()
        # set serial port
        comx.port = self.options.serialPort
        # set baudrate
        comx.baudrate = self.options.serialBaudRate
        # set bytesize
        if self.options.serialByteSize == 'five':
            comx.bytesize = serial.FIVEBITS
        if self.options.serialByteSize == 'six':
            comx.bytesize = serial.SIXBITS
        if self.options.serialByteSize == 'seven':
            comx.bytesize = serial.SEVENBITS
        if self.options.serialByteSize == 'eight':
            comx.bytesize = serial.EIGHTBITS
        # set stopbits
        if self.options.serialStopBits == 'one':
            comx.stopbits = serial.STOPBITS_ONE
        if self.options.serialStopBits == 'onePointFive':
            comx.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        if self.options.serialStopBits == 'two':
            comx.stopbits = serial.STOPBITS_TWO
        # set parity
        if self.options.serialParity == 'none':
            comx.parity = serial.PARITY_NONE
        if self.options.serialParity == 'even':
            comx.parity = serial.PARITY_EVEN
        if self.options.serialParity == 'odd':
            comx.parity = serial.PARITY_ODD
        if self.options.serialParity == 'mark':
            comx.parity = serial.PARITY_MARK
        if self.options.serialParity == 'space':
            comx.parity = serial.PARITY_SPACE
        # set short timeout to avoid locked up interface
        comx.timeout = 0.1
        # set flow control
        if self.options.serialFlowControl == 'xonxoff':
            comx.xonxoff = True
        if self.options.serialFlowControl in ('rtscts', 'dsrdtrrtscts'):
            comx.rtscts = True
        if self.options.serialFlowControl == 'dsrdtrrtscts':
            comx.dsrdtr = True
        # try to establish connection
        try:
            comx.open()
        except serial.SerialException:
            inkex.errormsg(_("Could not open port. Please check that your plotter is "
                             "running, connected and the settings are correct."))
            return
        # send data to plotter
        comx.write(self.hpgl)
        comx.read(2)
        comx.close()

if __name__ == '__main__':
    Plot().run()

