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
from inkex import Script
from inkex.utils import NSS

NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

class Install(inkex.EffectExtension):
    """Install jessyInk extension into an SVG"""
    def add_arguments(self, pars):
        pars.add_argument('--tab', type=str, dest='what')

    def effect(self):
        # Find and delete old script node
        for node in self.svg.xpath("//svg:script[@id='JessyInk']"):
            node.getparent().remove(node)

        # Create new script node
        script_elem = Script()
        with open(self.get_resource("jessyInk.js")) as fhl:
            script_elem.text = fhl.read()
        script_elem.set("id", "JessyInk")
        script_elem.set("jessyink:version", '1.5.5')
        self.svg.append(script_elem)

        # Remove "jessyInkInit()" in the "onload" attribute, if present.
        prop_list = [prop.strip() for prop in self.svg.get("onload", '').split(';')]
        if "jessyInkInit()" in prop_list:
            prop_list.remove("jessyInkInit()")
        self.svg.set("onload", "; ".join(prop_list) or None)

        # Update jessyInk attributes to new formats
        for attr in ('effectIn', 'effectOut', 'masterSlide',
                     'transitionIn', 'transitionOut', 'autoText'):
            self._update_attr(attr)

    def _update_attr(self, name):
        """Update a single attr"""
        for node in self.svg.xpath(f"//*[@jessyInk_{name}]"):
            node.attrib[f"jessyink:{name}"] = node.attrib[f"jessyInk_{name}"]
            del node.attrib[f"jessyInk_{name}"]
        for node in self.svg.xpath(f"//*[@jessyink:{name}]"):
            node.attrib[f"jessyink:{name}"] = node.attrib[f"jessyink:{name}"].replace("=", ":")

# Create effect instance
if __name__ == '__main__':
    Install().run()
