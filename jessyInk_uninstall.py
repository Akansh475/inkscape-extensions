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
from inkex.utils import NSS

NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

def propStrToList(str):
    list = []
    propList = str.split(";")
    for prop in propList:
        if not (len(prop) == 0):
            list.append(prop.strip())
    return list

def listToPropStr(list):
    str = ""
    for prop in list:
        str += " " + prop + ";"
    return str[1:]

class Uninstall(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--tab',  type=str, dest = 'what')
        pars.add_argument('--remove_script',  type=inkex.Boolean, dest = 'remove_script', default = True)
        pars.add_argument('--remove_effects',  type=inkex.Boolean, dest = 'remove_effects', default = True)
        pars.add_argument('--remove_masterSlide',  type=inkex.Boolean, dest = 'remove_masterSlide', default = True)
        pars.add_argument('--remove_transitions',  type=inkex.Boolean, dest = 'remove_transitions', default = True)
        pars.add_argument('--remove_autoTexts',  type=inkex.Boolean, dest = 'remove_autoTexts', default = True)
        pars.add_argument('--remove_views',  type=inkex.Boolean, dest = 'remove_views', default = True)


    def effect(self):
        # Remove script, if so desired.
        if self.options.remove_script:
            # Find and delete script node.
            for node in self.document.xpath("//svg:script[@id='JessyInk']", namespaces=NSS):
                node.getparent().remove(node)

            # Remove "jessyInkInit()" in the "onload" attribute, if present.
            if self.document.getroot().get("onload"):
                propList = propStrToList(self.document.getroot().get("onload"))
            else:
                propList = []

            for prop in propList:
                if prop == "jessyInkInit()":
                    propList.remove("jessyInkInit()")

            if len(propList) > 0:
                self.document.getroot().set("onload", listToPropStr(propList))
            else:
                if self.document.getroot().get("onload"):
                    del self.document.getroot().attrib["onload"]

        # Remove effect attributes, if so desired.
        if self.options.remove_effects:
            for node in self.document.xpath("//*[@jessyink:effectIn]", namespaces=NSS):
                del node.attrib["{" + NSS["jessyink"] + "}effectIn"]

            for node in self.document.xpath("//*[@jessyink:effectOut]", namespaces=NSS):
                del node.attrib["{" + NSS["jessyink"] + "}effectOut"]

            # Remove old style attributes as well.
            for node in self.document.xpath("//*[@jessyInk_effectIn]", namespaces=NSS):
                del node.attrib["jessyInk_effectIn"]

            for node in self.document.xpath("//*[@jessyInk_effectOut]", namespaces=NSS):
                del node.attrib["jessyInk_effectOut"]

        # Remove master slide assignment, if so desired.
        if self.options.remove_masterSlide:
            for node in self.document.xpath("//*[@jessyink:masterSlide]", namespaces=NSS):
                del node.attrib["{" + NSS["jessyink"] + "}masterSlide"]

            # Remove old style attributes as well.
            for node in self.document.xpath("//*[@jessyInk_masterSlide]", namespaces=NSS):
                del node.attrib["jessyInk_masterSlide"]

        # Remove transitions, if so desired.
        if self.options.remove_transitions:
            for node in self.document.xpath("//*[@jessyink:transitionIn]", namespaces=NSS):
                del node.attrib["{" + NSS["jessyink"] + "}transitionIn"]

            for node in self.document.xpath("//*[@jessyink:transitionOut]", namespaces=NSS):
                del node.attrib["{" + NSS["jessyink"] + "}transitionOut"]

            # Remove old style attributes as well.
            for node in self.document.xpath("//*[@jessyInk_transitionIn]", namespaces=NSS):
                del node.attrib["jessyInk_transitionIn"]

            for node in self.document.xpath("//*[@jessyInk_transitionOut]", namespaces=NSS):
                del node.attrib["jessyInk_transitionOut"]

        # Remove auto texts, if so desired.
        if self.options.remove_autoTexts:
            for node in self.document.xpath("//*[@jessyink:autoText]", namespaces=NSS):
                del node.attrib["{" + NSS["jessyink"] + "}autoText"]

            # Remove old style attributes as well.
            for node in self.document.xpath("//*[@jessyInk_autoText]", namespaces=NSS):
                del node.attrib["jessyInk_autoText"]

        # Remove views, if so desired.
        if self.options.remove_views:
            for node in self.document.xpath("//*[@jessyink:view]", namespaces=NSS):
                del node.attrib["{" + NSS["jessyink"] + "}view"]


# Create effect instance.
if __name__ == '__main__':
    Uninstall().run()
