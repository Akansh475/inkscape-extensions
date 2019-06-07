#!/usr/bin/env python
# coding=utf-8
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
from inkex.localization import _

class JessyInk_Effects(inkex.Effect):
    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        self.arg_parser.add_argument('--tab',  type=str, dest = 'what')
        self.arg_parser.add_argument('--effectInOrder',  type=str, dest = 'effectInOrder', default = 1)
        self.arg_parser.add_argument('--effectInDuration',  type=float, dest = 'effectInDuration', default = 0.8)
        self.arg_parser.add_argument('--effectIn',  type=str, dest = 'effectIn', default = 'none')
        self.arg_parser.add_argument('--effectOutOrder',  type=str, dest = 'effectOutOrder', default = 2)
        self.arg_parser.add_argument('--effectOutDuration',  type=float, dest = 'effectOutDuration', default = 0.8)
        self.arg_parser.add_argument('--effectOut',  type=str, dest = 'effectOut', default = 'none')

        inkex.NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=inkex.NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        if len(self.svg.selected) == 0:
            inkex.errormsg(_("No object selected. Please select the object you want to assign an effect to and then press apply.\n"))

        for id, node in self.svg.selected.items():
            if (self.options.effectIn == "appear") or (self.options.effectIn == "fade") or (self.options.effectIn == "pop"):
                node.set("{" + inkex.NSS["jessyink"] + "}effectIn","name:" + self.options.effectIn  + ";order:" + self.options.effectInOrder + ";length:" + str(int(self.options.effectInDuration * 1000)))
                # Remove possible view argument.
                if "{" + inkex.NSS["jessyink"] + "}view" in node.attrib:
                    del node.attrib["{" + inkex.NSS["jessyink"] + "}view"]
            else:
                if "{" + inkex.NSS["jessyink"] + "}effectIn" in node.attrib:
                    del node.attrib["{" + inkex.NSS["jessyink"] + "}effectIn"]

            if (self.options.effectOut == "appear") or (self.options.effectOut == "fade") or (self.options.effectOut == "pop"):
                node.set("{" + inkex.NSS["jessyink"] + "}effectOut","name:" + self.options.effectOut  + ";order:" + self.options.effectOutOrder + ";length:" + str(int(self.options.effectOutDuration * 1000)))
                # Remove possible view argument.
                if "{" + inkex.NSS["jessyink"] + "}view" in node.attrib:
                    del node.attrib["{" + inkex.NSS["jessyink"] + "}view"]
            else:
                if "{" + inkex.NSS["jessyink"] + "}effectOut" in node.attrib:
                    del node.attrib["{" + inkex.NSS["jessyink"] + "}effectOut"]

# Create effect instance
if __name__ == '__main__':
    JessyInk_Effects().run()

