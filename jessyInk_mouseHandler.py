#!/usr/bin/env python
# Copyright 2008, 2009 Hannes Hochreiner
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

import os

import sys

# We will use the inkex module with the predefined Effect base class.
import inkex


class JessyInk_CustomMouseHandler(inkex.Effect):
    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        self.arg_parser.add_argument('--tab', action = 'store', type=str, dest = 'what')
        self.arg_parser.add_argument('--mouseSettings', action = 'store', type=str, dest = 'mouseSettings', default = 'default')

        inkex.NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=inkex.NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        # Remove old mouse handler
        for node in self.document.xpath("//jessyink:mousehandler", namespaces=inkex.NSS):
            node.getparent().remove(node)

        if self.options.mouseSettings == "noclick":
            # Create new script node.
            scriptElm = inkex.etree.Element(inkex.addNS("script", "svg"))
            scriptElm.text = open(os.path.join(os.path.dirname(__file__), "jessyInk_core_mouseHandler_noclick.js")).read()
            groupElm = inkex.etree.Element(inkex.addNS("mousehandler", "jessyink"))
            groupElm.set("{" + inkex.NSS["jessyink"] + "}subtype", "jessyInk_core_mouseHandler_noclick")
            groupElm.append(scriptElm)
            self.document.getroot().append(groupElm)
        elif self.options.mouseSettings == "draggingZoom":
            # Create new script node.
            scriptElm = inkex.etree.Element(inkex.addNS("script", "svg"))
            scriptElm.text = open(os.path.join(os.path.dirname(__file__), "jessyInk_core_mouseHandler_zoomControl.js")).read()
            groupElm = inkex.etree.Element(inkex.addNS("mousehandler", "jessyink"))
            groupElm.set("{" + inkex.NSS["jessyink"] + "}subtype", "jessyInk_core_mouseHandler_zoomControl")
            groupElm.append(scriptElm)
            self.document.getroot().append(groupElm)

# Create effect instance
if __name__ == '__main__':
    effect = JessyInk_CustomMouseHandler()
    effect.affect()

