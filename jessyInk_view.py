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

import inkex
from inkex.localization import inkex_gettext as _
from inkex.utils import NSS
NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

def propStrToList(str):
    list = []
    propList = str.split(";")
    for prop in propList:
        if not (len(prop) == 0):
            list.append(prop.strip())
    return list

def propListToDict(list):
    dictio = {}

    for prop in list:
        keyValue = prop.split(":")

        if len(keyValue) == 2:
            dictio[keyValue[0].strip()] = keyValue[1].strip()

    return dictio

class View(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--tab', dest='what')
        pars.add_argument('--viewOrder', type=int, default=1)
        pars.add_argument('--viewDuration', type=float, default=0.8)
        pars.add_argument('--removeView', type=inkex.Boolean)

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        rect = None

        for id, node in self.svg.selected.items():
            if rect != None:
                raise inkex.AbortExtension(_("More than one object selected. Please select only one object.\n"))
            rect = node

        if rect == None:
            raise inkex.AbortExtension(_("No object selected. Please select the object you want to assign a view to and then press apply.\n"))

        if not self.options.removeView:
            viewOrder = str(self.options.viewOrder)
            # Remove the view that currently has the requested order number.
            for node in rect.xpath("ancestor::svg:g[@inkscape:groupmode='layer']/descendant::*[@jessyink:view]", namespaces=NSS):
                propDict = propListToDict(propStrToList(node.attrib["{" + NSS["jessyink"] + "}view"]))

                if propDict["order"] == viewOrder:
                    del node.attrib["{" + NSS["jessyink"] + "}view"]

            # Set the new view.
            rect.set("{" + NSS["jessyink"] + "}view","name:view;order:" + viewOrder + ";length:" + str(int(self.options.viewDuration * 1000)))

            # Remove possible effect arguments.
            if "{" + NSS["jessyink"] + "}effectIn" in rect.attrib:
                del rect.attrib["{" + NSS["jessyink"] + "}effectIn"]

            if "{" + NSS["jessyink"] + "}effectOut" in rect.attrib:
                del rect.attrib["{" + NSS["jessyink"] + "}effectOut"]
        else:
            if "{" + NSS["jessyink"] + "}view" in node.attrib:
                del node.attrib["{" + NSS["jessyink"] + "}view"]

if __name__ == '__main__':
    View().run()
