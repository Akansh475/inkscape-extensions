#!/usr/bin/env python
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

import inkex
from inkex.utils import NSS

NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

class MasterSlide(inkex.EffectExtension):
    def add_arguments(self, pars):
        self.arg_parser.add_argument('--tab', dest='what')
        self.arg_parser.add_argument('--layerName', default='')

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        # Remove old master slide property
        for node in self.document.xpath("//*[@jessyink:masterSlide='masterSlide']", namespaces=NSS):
            del node.attrib["{" + NSS["jessyink"] + "}masterSlide"]

        # Set new master slide.
        if self.options.layerName != "":
            nodes = self.document.xpath("//*[@inkscape:groupmode='layer' and @inkscape:label='" + self.options.layerName + "']", namespaces=NSS)
            if len(nodes) == 0:
                inkex.errormsg(_("Layer not found. Removed current master slide selection.\n"))
            elif len(nodes) > 1:
                inkex.errormsg(_("More than one layer with this name found. Removed current master slide selection.\n"))
            else:
                nodes[0].set("{" + NSS["jessyink"] + "}masterSlide","masterSlide")

if __name__ == '__main__':
    MasterSlide().run()
