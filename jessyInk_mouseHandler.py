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
#

import os

from lxml import etree

import inkex
from inkex.utils import NSS
NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

class MouseHandler(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--tab', dest='what')
        pars.add_argument('--mouseSetting', default='default')

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        # Remove old mouse handler
        for node in self.document.xpath("//jessyink:mousehandler", namespaces=NSS):
            node.getparent().remove(node)

        if self.options.mouseSetting == "noclick":
            # Create new script node.
            scriptElm = etree.Element(inkex.addNS("script", "svg"))
            scriptElm.text = open(os.path.join(os.path.dirname(__file__), "jessyInk_core_mouseHandler_noclick.js")).read()
            groupElm = etree.Element(inkex.addNS("mousehandler", "jessyink"))
            groupElm.set("{" + NSS["jessyink"] + "}subtype", "jessyInk_core_mouseHandler_noclick")
            groupElm.append(scriptElm)
            self.document.getroot().append(groupElm)
        elif self.options.mouseSetting == "draggingZoom":
            # Create new script node.
            scriptElm = etree.Element(inkex.addNS("script", "svg"))
            scriptElm.text = open(os.path.join(os.path.dirname(__file__), "jessyInk_core_mouseHandler_zoomControl.js")).read()
            groupElm = etree.Element(inkex.addNS("mousehandler", "jessyink"))
            groupElm.set("{" + NSS["jessyink"] + "}subtype", "jessyInk_core_mouseHandler_zoomControl")
            groupElm.append(scriptElm)
            self.document.getroot().append(groupElm)


# Create effect instance
if __name__ == '__main__':
    MouseHandler().run()
