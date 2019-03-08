#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
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
import math

from lxml import etree

import inkex


class Dots(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("-d", "--dotsize",
                                     type=str,
                                     dest="dotsize", default="10px",
                                     help="Size of the dots placed at path nodes")
        self.arg_parser.add_argument("-f", "--fontsize",
                                     type=str,
                                     dest="fontsize", default="20",
                                     help="Size of node label numbers")
        self.arg_parser.add_argument("-s", "--start",
                                     type=int,
                                     dest="start", default="1",
                                     help="First number in the sequence, assigned to the first node")
        self.arg_parser.add_argument("-t", "--step",
                                     type=int,
                                     dest="step", default="1",
                                     help="Numbering step between two nodes")
        self.arg_parser.add_argument("--tab",
                                     type=str,
                                     dest="tab",
                                     help="The selected UI-tab when OK was pressed")

    def effect(self):
        selection = self.svg.selected
        if selection:
            for id, node in selection.items():
                if node.tag == inkex.addNS('path', 'svg'):
                    self.addDot(node)
        else:
            inkex.errormsg("Please select an object.")

    def separateLastAndFirst(self, p):
        # Separate the last and first dot if they are together
        lastDot = -1
        if not p[lastDot][1]:
            lastDot = -2
        if round(p[lastDot][1][-2]) == round(p[0][1][-2]) and \
                round(p[lastDot][1][-1]) == round(p[0][1][-1]):
            x1 = p[lastDot][1][-2]
            y1 = p[lastDot][1][-1]
            x2 = p[lastDot - 1][1][-2]
            y2 = p[lastDot - 1][1][-1]
            dx = abs(max(x1, x2) - min(x1, x2))
            dy = abs(max(y1, y2) - min(y1, y2))
            dist = math.sqrt(dx ** 2 + dy ** 2)
            x = dx / dist
            y = dy / dist
            if x1 > x2:
                x *= -1
            if y1 > y2:
                y *= -1
            p[lastDot][1][-2] += x * self.svg.unittouu(self.options.dotsize)
            p[lastDot][1][-1] += y * self.svg.unittouu(self.options.dotsize)

    def addDot(self, node):
        self.group = etree.SubElement(node.getparent(), inkex.addNS('g', 'svg'))
        self.dotGroup = etree.SubElement(self.group, inkex.addNS('g', 'svg'))
        self.numGroup = etree.SubElement(self.group, inkex.addNS('g', 'svg'))

        try:
            t = node.get('transform')
            self.group.set('transform', t)
        except:
            pass

        style = str(inkex.Style({'stroke': 'none', 'fill': '#000'}))
        p = inkex.parsePath(node.get('d'))

        self.separateLastAndFirst(p)

        num = self.options.start
        for cmd, params in p:
            if cmd != 'Z' and cmd != 'z':
                dot_att = {
                    'style': style,
                    'r': str(self.svg.unittouu(self.options.dotsize) / 2),
                    'cx': str(params[-2]),
                    'cy': str(params[-1])
                }
                etree.SubElement(
                        self.dotGroup,
                        inkex.addNS('circle', 'svg'),
                        dot_att)
                self.addText(
                        self.numGroup,
                        params[-2] + (self.svg.unittouu(self.options.dotsize) / 2),
                        params[-1] - (self.svg.unittouu(self.options.dotsize) / 2),
                        num)
                num += self.options.step
        node.getparent().remove(node)

    def addText(self, node, x, y, text):
        new = etree.SubElement(node, inkex.addNS('text', 'svg'))
        s = {'font-size': self.svg.unittouu(self.options.fontsize),
             'fill-opacity': '1.0',
             'stroke': 'none',
             'font-weight': 'normal',
             'font-style': 'normal',
             'fill': '#999'}
        new.set('style', str(inkex.Style(s)))
        new.set('x', str(x))
        new.set('y', str(y))
        new.text = str(text)


if __name__ == '__main__':
    Dots().run()
