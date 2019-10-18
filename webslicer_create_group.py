#!/usr/bin/env python
#
# Copyright (C) 2010 Aurelio A. Heckert, aurium (a) gmail dot com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
from lxml import etree

import inkex
from webslicer_effect import WebSlicerMixin, is_empty


class WebSlicer_CreateGroup(WebSlicerMixin, inkex.EffectExtension):

    def __init__(self):
        super(WebSlicer_CreateGroup, self).__init__()
        self.arg_parser.add_argument("--html-id",
                                     type=str,
                                     dest="html_id",
                                     help="")
        self.arg_parser.add_argument("--html-class",
                                     type=str,
                                     dest="html_class",
                                     help="")
        self.arg_parser.add_argument("--width-unity",
                                     type=str,
                                     dest="width_unity",
                                     help="")
        self.arg_parser.add_argument("--height-unity",
                                     type=str,
                                     dest="height_unity",
                                     help="")
        self.arg_parser.add_argument("--bg-color",
                                     type=str,
                                     dest="bg_color",
                                     help="")
        self.arg_parser.add_argument("--tab",
                                     type=str,
                                     dest="tab",
                                     help="The selected UI-tab when OK was pressed")

    def get_base_elements(self):
        self.layer = self.get_slicer_layer()
        if is_empty(self.layer):
            return inkex.errormsg(_('You must create and select some "Slicer rectangles" before trying to group.'))
        self.layer_descendants = self.get_descendants_in_array(self.layer)

    def get_descendants_in_array(self, el):
        descendants = el.getchildren()
        for e in descendants:
            descendants.extend(self.get_descendants_in_array(e))
        return descendants

    def effect(self):
        self.get_base_elements()
        if not self.svg.selected:
            return inkex.errormsg(_('You must to select some "Slicer rectangles" or other "Layout groups".'))
        for key, node in self.svg.selected.items():
            if node not in self.layer_descendants:
                return inkex.errormsg(_('Oops... The element "%s" is not in the Web Slicer layer') % key)
        g_parent = node.getparent()
        group = etree.SubElement(g_parent, 'g')
        desc = etree.SubElement(group, 'desc')
        desc.text = self.get_conf_text_from_list(
                ['html_id', 'html_class',
                 'width_unity', 'height_unity',
                 'bg_color'])

        for node in self.svg.selected.values():
            group.insert(1, node)


if __name__ == '__main__':
    WebSlicer_CreateGroup().run()
