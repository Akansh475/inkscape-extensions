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
from inkex.elements import BaseElement, Script
from inkex.utils import NSS

NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

class MouseHandler(BaseElement):
    """jessyInk mouse handler"""
    tag_name = 'jessyink:mousehandler'

class AddMouseHandler(inkex.EffectExtension):
    """Add mouse handler"""
    def add_arguments(self, pars):
        pars.add_argument('--tab')
        pars.add_argument('--mouseSetting', default='default')

    def effect(self):
        # Check version.
        scripts = self.svg.getElement("//svg:script[@jessyink:version='1.5.5']")
        if scripts is None:
            raise inkex.AbortExtension(_(
                "The JessyInk script is not installed in this SVG file or has a "
                "different version than the JessyInk extensions. Please select "
                "\"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" "
                "menu to install or update the JessyInk script.\n\n"))

        # Remove old mouse handler
        for node in self.svg.xpath("//jessyink:mousehandler"):
            node.getparent().remove(node)

        # Create new script node.
        script = Script()
        group = MouseHandler()

        if self.options.mouseSetting == "noclick":
            name = "noclick"
        elif self.options.mouseSetting == "draggingZoom":
            name = "zoomControl"
        elif self.options.mouseSetting == "default":
            # Default is to remove script and continue
            return

        with open(self.get_resource(f"jessyInk_core_mouseHandler_{name}.js")) as fhl:
            script.text = fhl.read()
        group.set("jessyink:subtype", f"jessyInk_core_mouseHandler_{name}")

        group.append(script)
        self.svg.append(group)

# Create effect instance
if __name__ == '__main__':
    AddMouseHandler().run()
