#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2013 Nicolas Dufour (jazzynico)
# Direction code from the Restack extension, by Rob Antonishen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import csv
import os
from subprocess import PIPE, Popen

from lxml import etree

import inkex
from inkex import inkbool


class Merge(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("-d", "--direction",
                                     type=str,
                                     dest="direction", default="tb",
                                     help="direction to merge text")
        self.arg_parser.add_argument("-x", "--xanchor",
                                     type=str,
                                     dest="xanchor", default="m",
                                     help="horizontal point to compare")
        self.arg_parser.add_argument("-y", "--yanchor",
                                     type=str,
                                     dest="yanchor", default="m",
                                     help="vertical point to compare")
        self.arg_parser.add_argument("-t", "--flowtext",
                                     type=inkbool,
                                     dest="flowtext", default=False,
                                     help="use a flow text structure instead of a normal text element")
        self.arg_parser.add_argument("-k", "--keepstyle",
                                     type=inkbool,
                                     dest="keepstyle", default=False,
                                     help="keep format")

    def effect(self):
        if not self.svg.selected:
            for node in self.document.xpath('//svg:text | //svg:flowRoot', namespaces=inkex.NSS):
                self.svg.selected[node.get('id')] = node

        if self.svg.selected:
            parentnode = self.svg.get_current_layer()
            objlist = []
            # calculate distances for each selected object
            for node in self.svg.selected.values():
                # get the bounding box
                bbox = node.bounding_box()
                if not bbox:
                    continue

                # calc the comparison coords
                if self.options.xanchor == "l":
                    cx = bbox.left
                elif self.options.xanchor == "r":
                    cx = bbox.right
                else:  # middle
                    cx = bbox.center()[0]

                if self.options.yanchor == "t":
                    cy = bbox.top
                elif self.options.yanchor == "b":
                    cy = bbox.bottom
                else:  # middle
                    cy = bbox.center()[1]

                # direction chosen
                if self.options.direction == "tb":
                    objlist.append([cy, node])
                elif self.options.direction == "bt":
                    objlist.append([-cy, node])
                elif self.options.direction == "lr":
                    objlist.append([cx, node])
                elif self.options.direction == "rl":
                    objlist.append([-cx, node])

            objlist.sort(key=lambda x: x[0])
            # move them to the top of the object stack in this order.

            if self.options.flowtext:
                self.text_element = "flowRoot"
                self.text_span = "flowPara"
            else:
                self.text_element = "text"
                self.text_span = "tspan"

            self.textRoot = etree.SubElement(parentnode, inkex.addNS(self.text_element, 'svg'), {inkex.addNS('space', 'xml'): 'preserve'})
            self.textRoot.set(inkex.addNS('style', ''), 'font-size:20px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;')

            for _, node in objlist:
                self.recurse(node, self.textRoot)

            if self.options.flowtext:
                self.region = etree.SubElement(self.textRoot, inkex.addNS('flowRegion', 'svg'), {inkex.addNS('space', 'xml'): 'preserve'})
                self.rect = etree.SubElement(self.region, inkex.addNS('rect', 'svg'), {inkex.addNS('space', 'xml'): 'preserve'})
                self.rect.set(inkex.addNS('height', ''), '200')
                self.rect.set(inkex.addNS('width', ''), '200')

    def recurse(self, node, span):
        # istext = (node.tag == '{http://www.w3.org/2000/svg}flowPara' or node.tag == '{http://www.w3.org/2000/svg}flowDiv' or node.tag == '{http://www.w3.org/2000/svg}tspan')
        if node.tag != '{http://www.w3.org/2000/svg}flowRegion':

            newspan = etree.SubElement(span, inkex.addNS(self.text_span, 'svg'), {inkex.addNS('space', 'xml'): 'preserve'})

            if node.get('{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}role'):
                newspan.set(inkex.addNS('role', 'sodipodi'), node.get('{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}role'))
            if node.tag == '{http://www.w3.org/2000/svg}text' or node.tag == '{http://www.w3.org/2000/svg}flowPara':
                newspan.set(inkex.addNS('role', 'sodipodi'), 'line')

            if self.options.keepstyle:
                if node.get('style'):
                    newspan.set(inkex.addNS('style', ''), node.get('style'))

            if node.text is not None:
                newspan.text = node.text
            for child in node:
                self.recurse(child, newspan)
            if node.tail and node.tag != '{http://www.w3.org/2000/svg}text':
                newspan.tail = node.tail


if __name__ == '__main__':
    Merge().run()
