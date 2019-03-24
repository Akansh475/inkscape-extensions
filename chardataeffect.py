#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2006 Jos Hirth, kaioa.com
# Copyright (C) 2007 bulia byak
# Copyright (C) 2007 Aaron C. Spike
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
import inkex

TEXT_TAGS = (
    inkex.addNS('svg:flowPara'),
    inkex.addNS('svg:flowDiv'),
    inkex.addNS('svg:text'),
)

SODIPODI_ROLE = inkex.addNS('sodipodi:role')


class CharEffectBase(inkex.Effect):
    """Base class for all char effects"""
    def __init__(self):
        inkex.Effect.__init__(self)
        self.visited = []

    newline = True
    newpar = True

    def effect(self):
        nodes = self.svg.selected or {None: self.document.getroot()}
        for node in nodes.values():
            self.recurse(node)

    def recurse(self, node):
        """Reverse the node text"""
        if node.get(SODIPODI_ROLE) == 'line':
            self.newline = True
        elif node.tag in TEXT_TAGS:
            self.newline = True
            self.newpar = True

        if node.text is not None:
            node.text = self.process_chardata(node.text)
            self.newline = False
            self.newpar = False

        for child in node:
            self.recurse(child)

        if node.tail is not None:
            node.tail = self.process_chardata(node.tail)

    def process_chardata(self, text):
        """Replacable chardata method for processing the text"""
        return ''.join(map(self.map_char, text))

    @staticmethod
    def map_char(char):
        """Replaceable map_char method for processing each letter"""
        raise NotImplementedError("Please provide a process_chardata or map_char static method.")
