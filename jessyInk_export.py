#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2008, 2009 Hannes Hochreiner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#
"""
JessyInk Export to zipfile multiple layers.
"""

import zipfile

import inkex
from inkex.localization import _
from inkex.base import TempDirMixin
from inkex.generic import OutputExtension
from inkex.command import take_snapshot
from inkex.utils import NSS

class JessyInkExport(TempDirMixin, OutputExtension):
    """
    JessyInkExport Output Extension saves to a zipfile each of the layers.
    """
    dir_prefix = 'jessyInk-'

    def __init__(self):
        super(JessyInkExport, self).__init__()

        self.arg_parser.add_argument('--tab', type=str, dest='what')
        self.arg_parser.add_argument('--type', type=str, dest='type', default='png')
        self.arg_parser.add_argument('--resolution', type=str, dest='resolution', default='1.0')

        # Register jessyink namespace.
        NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

    def save(self, stream):
        # Check whether the JessyInk-script is present (indicating
        # that the presentation has not been properly exported).
        script = self.svg.xpath("//svg:script[@jessyink:version]")

        if script:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has"
                             " a different version than the JessyInk extensions. Please"
                             " select \"install/update...\" from the \"JessyInk\" sub-menu"
                             " of the \"Extensions\" menu to install or update the JessyInk"
                             " script.\n\n"))

        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as output:

            # Find layers.
            layers = self.svg.xpath("//svg:g[@inkscape:groupmode='layer']")

            if len(layers) < 1:
                inkex.errormsg("No layers found.")
                return

            for node in layers:
                # Make all layers invisible
                node.style['display'] = "none"

            for node in layers:
                # Show only one layer at a time.
                node.style.update("display:inherit;opacity:1")

                name = node.get('inkscape:label')
                newname = "{}.{}".format(name, self.options.type)
                filename = take_snapshot(self.document, dirname=self.tempdir,
                                         name=name, ext=self.options.type,
                                         dpi=self.options.resolution)
                output.write(filename, newname)

                node.style['display'] = "none"


if __name__ == '__main__':
    JessyInkExport().run()
