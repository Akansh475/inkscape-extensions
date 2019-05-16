#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2011 Nicolas Dufour (jazzynico)
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
#

import copy
import sys

from lxml import etree

import inkex


class Extract(inkex.Effect):
    def __init__(self):
        super(Extract, self).__init__()
        self.arg_parser.add_argument("-d", "--direction",
                                     type=str,
                                     dest="direction", default="tb",
                                     help="direction to extract text")
        self.arg_parser.add_argument("-x", "--xanchor",
                                     type=str,
                                     dest="xanchor", default="m",
                                     help="horizontal point to compare")
        self.arg_parser.add_argument("-y", "--yanchor",
                                     type=str,
                                     dest="yanchor", default="m",
                                     help="vertical point to compare")

    def effect(self):
        if not self.svg.selected:
            for node in self.document.xpath('//svg:text | //svg:flowRoot', namespaces=inkex.NSS):
                self.svg.selected[node.get('id')] = node

        if self.svg.selected:
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
            for _, node in objlist:
                self.recurse(copy.deepcopy(node))

    def recurse(self, node):
        istext = (node.tag == '{http://www.w3.org/2000/svg}flowPara' or node.tag == '{http://www.w3.org/2000/svg}flowDiv' or node.tag == '{http://www.w3.org/2000/svg}text')
        if node.text is not None or node.tail is not None:
            for child in node:
                if child.get('{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}role'):
                    child.tail = "\n"
            inkex.errormsg(etree.tostring(node, encoding='unicode', method='text').strip())
        else:
            for child in node:
                self.recurse(child)


if __name__ == '__main__':
    Extract().run()
