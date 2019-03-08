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

import sys

# We will use the inkex module with the predefined Effect base class.
import inkex


class JessyInk_Transitions(inkex.Effect):
    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        self.arg_parser.add_argument('--tab', action = 'store', type=str, dest = 'what')
        self.arg_parser.add_argument('--layerName', action = 'store', type=str, dest = 'layerName', default = '')
        self.arg_parser.add_argument('--effectIn', action = 'store', type=str, dest = 'effectIn', default = 'default')
        self.arg_parser.add_argument('--effectInDuration', action = 'store', type=float, dest = 'effectInDuration', default = 0.8)
        self.arg_parser.add_argument('--effectOut', action = 'store', type=str, dest = 'effectOut', default = 'default')
        self.arg_parser.add_argument('--effectOutDuration', action = 'store', type=float, dest = 'effectOutDuration', default = 0.8)

        inkex.NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=inkex.NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        if self.options.layerName != "":
            nodes = self.document.xpath(u"//*[@inkscape:groupmode='layer' and @inkscape:label='" + self.options.layerName + "']", namespaces=inkex.NSS)
            if len(nodes) == 0:
                inkex.errormsg(_("Layer not found.\n"))
            elif len(nodes) > 1:
                inkex.errormsg(_("More than one layer with this name found.\n"))
            else:
                if self.options.effectIn == "default":
                    if nodes[0].get("{" + inkex.NSS["jessyink"] + "}transitionIn"):
                        del nodes[0].attrib["{" + inkex.NSS["jessyink"] + "}transitionIn"]
                else:
                    nodes[0].set("{" + inkex.NSS["jessyink"] + "}transitionIn","name:" + self.options.effectIn + ";length:" + str(int(self.options.effectInDuration * 1000)))
                if self.options.effectOut == "default":
                    if nodes[0].get("{" + inkex.NSS["jessyink"] + "}transitionOut"):
                        del nodes[0].attrib["{" + inkex.NSS["jessyink"] + "}transitionOut"]
                else:
                    nodes[0].set("{" + inkex.NSS["jessyink"] + "}transitionOut","name:" + self.options.effectOut + ";length:" + str(int(self.options.effectOutDuration * 1000)))
        else:
            inkex.errormsg(_("Please enter a layer name.\n"))

# Create effect instance
if __name__ == '__main__':

    effect = JessyInk_Transitions()
    effect.affect()

