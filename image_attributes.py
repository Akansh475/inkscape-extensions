#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2015, ~suv <suv-sf@users.sf.net>
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
"""
image_attributes.py - adjust image attributes which don't have global
GUI options yet

Tool for Inkscape 0.91 to adjust rendering of drawings with linked
or embedded bitmap images created with older versions of Inkscape
or third-party applications.
"""

# local library
import inkex
from inkex.utils import inkbool
from inkex.generic import EffectExtension


class SetAttrImage(inkex.Effect):
    def __init__(self):
        super(SetAttrImage, self).__init__()
        # main options
        self.arg_parser.add_argument("--fix_scaling", type=inkbool,
                                     dest="fix_scaling", default=True)
        self.arg_parser.add_argument("--fix_rendering", type=inkbool,
                                     dest="fix_rendering", default=False)
        self.arg_parser.add_argument("--aspect_ratio", type=str,
                                     dest="aspect_ratio", default="none",
                                     help="Value for attribute 'preserveAspectRatio'")
        self.arg_parser.add_argument("--aspect_clip", type=str,
                                     dest="aspect_clip", default="unset",
                                     help="optional 'meetOrSlice' value")
        self.arg_parser.add_argument("--aspect_ratio_scope", type=str,
                                     dest="aspect_ratio_scope", default="selected_only",
                                     help="scope within which to edit 'preserveAspectRatio' attr")
        self.arg_parser.add_argument("--image_rendering", type=str,
                                     dest="image_rendering", default="unset",
                                     help="Value for attribute 'image-rendering'")
        self.arg_parser.add_argument("--image_rendering_scope", type=str,
                                     dest="image_rendering_scope", default="selected_only",
                                     help="scope within which to edit 'image-rendering' attribute")
        # tabs
        self.arg_parser.add_argument("--tab_main", type=str, dest="tab_main")

    # core method

    def change_attribute(self, node, attribute):
        for key, value in attribute.items():
            if key == 'preserveAspectRatio':
                # set presentation attribute
                if value != "unset":
                    node.set(key, str(value))
                else:
                    if node.get(key):
                        del node.attrib[key]
            elif key == 'image-rendering':
                node_style = dict(inkex.Style.parse_str(node.get('style')))
                if key not in node_style:
                    # set presentation attribute
                    if value != "unset":
                        node.set(key, str(value))
                    else:
                        if node.get(key):
                            del node.attrib[key]
                else:
                    # set style property
                    if value != "unset":
                        node_style[key] = str(value)
                    else:
                        del node_style[key]
                    node.set('style', str(inkex.Style(node_style)))
            else:
                pass

    def change_all_images(self, node, attribute):
        path = 'descendant-or-self::svg:image'
        for img in node.xpath(path):
            self.change_attribute(img, attribute)

    # methods called via dispatcher

    def change_selected_only(self, selected, attribute):
        if selected:
            for node_id, node in selected.items():
                if node.tag == inkex.addNS('image', 'svg'):
                    self.change_attribute(node, attribute)

    def change_in_selection(self, selected, attribute):
        if selected:
            for node_id, node in selected.items():
                self.change_all_images(node, attribute)

    def change_in_document(self, selected, attribute):
        self.change_all_images(self.document.getroot(), attribute)

    def change_on_parent_group(self, selected, attribute):
        if selected:
            for node_id, node in selected.items():
                self.change_attribute(node.getparent(), attribute)

    def change_on_root_only(self, selected, attribute):
        self.change_attribute(self.document.getroot(), attribute)

    # main

    def effect(self):
        attr_val = []
        attr_dict = {}
        cmd_scope = None
        if self.options.tab_main == '"tab_basic"':
            cmd_scope = "in_document"
            attr_dict['preserveAspectRatio'] = ("none" if self.options.fix_scaling else "unset")
            attr_dict['image-rendering'] = ("optimizeSpeed" if self.options.fix_rendering else "unset")
        elif self.options.tab_main == '"tab_aspectRatio"':
            attr_val = [self.options.aspect_ratio]
            if self.options.aspect_clip != "unset":
                attr_val.append(self.options.aspect_clip)
            attr_dict['preserveAspectRatio'] = ' '.join(attr_val)
            cmd_scope = self.options.aspect_ratio_scope
        elif self.options.tab_main == '"tab_image_rendering"':
            attr_dict['image-rendering'] = self.options.image_rendering
            cmd_scope = self.options.image_rendering_scope
        else:  # help tab
            pass
        # dispatcher
        if cmd_scope is not None:
            try:
                change_cmd = getattr(self, 'change_{0}'.format(cmd_scope))
                change_cmd(self.selected, attr_dict)
            except AttributeError:
                inkex.errormsg('Scope "{0}" not supported'.format(cmd_scope))


if __name__ == '__main__':
    SetAttrImage().run()
