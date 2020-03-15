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


import inkex
from inkex.localization import inkex_gettext as _
from inkex.utils import NSS

NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

class JessyinkEffects(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--tab')
        pars.add_argument('--effectInOrder', type=int, default=1)
        pars.add_argument('--effectInDuration', type=float, default=0.8)
        pars.add_argument('--effectIn', default='none')
        pars.add_argument('--effectOutOrder', type=int, default=2)
        pars.add_argument('--effectOutDuration', type=float, default=0.8)
        pars.add_argument('--effectOut', default='none')

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=NSS)

        if len(scriptNodes) != 1:
            raise inkex.AbortExtension(
                _("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        if len(self.svg.selected) == 0:
            raise inkex.AbortExtension(
                _("No object selected. Please select the object you want to assign an effect to and then press apply.\n"))

        for id, node in self.svg.selected.items():
            if (self.options.effectIn == "appear") or (self.options.effectIn == "fade") or (self.options.effectIn == "pop"):
                node.set("{" + NSS["jessyink"] + "}effectIn","name:" + self.options.effectIn  + ";order:" + self.options.effectInOrder + ";length:" + str(int(self.options.effectInDuration * 1000)))
                # Remove possible view argument.
                if "{" + NSS["jessyink"] + "}view" in node.attrib:
                    del node.attrib["{" + NSS["jessyink"] + "}view"]
            else:
                if "{" + NSS["jessyink"] + "}effectIn" in node.attrib:
                    del node.attrib["{" + NSS["jessyink"] + "}effectIn"]

            if (self.options.effectOut == "appear") or (self.options.effectOut == "fade") or (self.options.effectOut == "pop"):
                node.set("{" + NSS["jessyink"] + "}effectOut","name:" + self.options.effectOut  + ";order:" + self.options.effectOutOrder + ";length:" + str(int(self.options.effectOutDuration * 1000)))
                # Remove possible view argument.
                if "{" + NSS["jessyink"] + "}view" in node.attrib:
                    del node.attrib["{" + NSS["jessyink"] + "}view"]
            else:
                if "{" + NSS["jessyink"] + "}effectOut" in node.attrib:
                    del node.attrib["{" + NSS["jessyink"] + "}effectOut"]

# Create effect instance
if __name__ == '__main__':
    JessyinkEffects().run()
