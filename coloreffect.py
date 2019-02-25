#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2006 Jos Hirth, kaioa.com
# Copyright (C) 2007 Aaron C. Spike
# Copyright (C) 2009 Monash University
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

from __future__ import absolute_import, division

import copy
import random

import inkex
import inkex.colors
from inkex.base import InkscapeExtension, SvgThroughMixin

color_props_fill = ('fill', 'stop-color', 'flood-color', 'lighting-color')
color_props_stroke = ('stroke',)
opacity_props = ('opacity',)  # 'stop-opacity', 'fill-opacity', 'stroke-opacity' don't work with clones
color_props = color_props_fill + color_props_stroke


class ColorEffect(SvgThroughMixin, InkscapeExtension):
    def __init__(self):
        super(ColorEffect, self).__init__()
        self.visited = []

    def effect(self):
        if not self.svg.selected:
            self.get_attribs(self.document.getroot())
        else:
            for node in self.svg.selected.values():
                self.get_attribs(node)

    def get_attribs(self, node):
        self.change_style(node)
        for child in node:
            self.get_attribs(child)

    def change_style(self, node):
        for attr in color_props:
            val = node.get(attr)
            if val:
                new_val = self.process_prop(val)
                if new_val != val:
                    node.set(attr, new_val)

        if 'style' in node.attrib:
            return self._style(node)

    def _style(self, node):
        # References for style attribute:
        # http://www.w3.org/TR/SVG11/styling.html#StyleAttribute,
        # http://www.w3.org/TR/CSS21/syndata.html
        #
        # The SVG spec is ambiguous as to how style attributes should be parsed.
        # For example, it isn't clear whether semicolons are allowed to appear
        # within strings or comments, or indeed whether comments are allowed to
        # appear at all.
        #
        # The processing here is just something simple that should usually work,
        # without trying too hard to get everything right.
        # (Won't work for the pathological case that someone escapes a property
        # name, probably does the wrong thing if colon or semicolon is used inside
        # a comment or string value.)
        style = node.get('style')  # fixme: this will break for presentation attributes!
        if style:
            declarations = style.split(';')
            opacity_in_style = False
            for i, decl in enumerate(declarations):
                parts = decl.split(':', 2)
                if len(parts) == 2:
                    (prop, val) = parts
                    prop = prop.strip().lower()
                    if prop in color_props:
                        val = val.strip()
                        new_val = self.process_prop(val)
                        if new_val != val:
                            declarations[i] = "{}:{}".format(prop, new_val)
                    elif prop in opacity_props:
                        opacity_in_style = True
                        val = val.strip()
                        new_val = self.process_prop(val)
                        if new_val != val:
                            declarations[i] = "{}:{}".format(prop, new_val)
            if not opacity_in_style:
                new_val = self.process_prop("1")
                declarations.append('opacity:{}'.format(new_val))
            node.set('style', ';'.join(declarations))

    def process_prop(self, col):
        if inkex.colors.is_color(col):
            c = inkex.colors.Color(col).to_rgb()
            col = '#{}'.format(self.colmod(c[0], c[1], c[2]))
        elif col.startswith('url(#'):
            id_ = col[len('url(#'):col.find(')')]
            new_id = '{}-{:d}'.format(id_, int(random.random() * 1000))
            path = '//*[@id="{}"]'.format(id_)
            for node in self.document.xpath(path, namespaces=inkex.NSS):
                self.process_gradient(node, new_id)
            col = 'url(#{})'.format(new_id)
        else:
            col = self.opacmod(col)

        return col

    def process_gradient(self, node, new_id):
        new_node = copy.deepcopy(node)
        new_node.set('id', new_id)
        node.getparent().append(new_node)
        self.change_style(new_node)
        for child in new_node:
            self.change_style(child)
        xlink = inkex.addNS('href', 'xlink')
        if xlink in new_node.attrib:
            href = new_node.get(xlink)
            if href.startswith('#'):
                id_ = href[len('#'):len(href)]
                new_href = '{}-{:d}'.format(id_, int(random.random() * 1000))
                new_node.set(xlink, '#{}'.format(new_href))
                path = '//*[@id="{}"]'.format(id_)
                for node in self.document.xpath(path, namespaces=inkex.NSS):
                    self.process_gradient(node, new_href)

    def colmod(self, r, g, b):
        raise NotImplementedError

    def opacmod(self, opacity):
        return opacity
