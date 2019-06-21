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
                                     dest="xanchor", default="center_x",
                                     help="horizontal point to compare")
        self.arg_parser.add_argument("-y", "--yanchor",
                                     type=str,
                                     dest="yanchor", default="center_y",
                                     help="vertical point to compare")

    def effect(self):
        if not self.svg.selected:
            for node in self.svg.xpath('//svg:text | //svg:flowRoot'):
                self.svg.selected[node.get('id')] = node

        if self.svg.selected:
            objlist = []

            # calculate distances for each selected object
            for node in self.svg.selected.values():
                # get the bounding box
                bbox = node.bounding_box()
                x = getattr(bbox, self.options.xanchor)
                y = getattr(bbox, self.options.yanchor)

                # direction chosen
                if self.options.direction == "tb":
                    objlist.append([y, node])
                elif self.options.direction == "bt":
                    objlist.append([-y, node])
                elif self.options.direction == "lr":
                    objlist.append([x, node])
                elif self.options.direction == "rl":
                    objlist.append([-x, node])

            objlist.sort(key=lambda x: x[0])
            # move them to the top of the object stack in this order.
            for _, node in objlist:
                self.recurse(node)

    def recurse(self, node):
        if node.text is not None or node.tail is not None:
            for child in node:
                if child.get('sodipodi:role'):
                    child.tail = "\n"
            inkex.errormsg(etree.tostring(node, encoding='unicode', method='text').strip())
        else:
            for child in node:
                self.recurse(child)


if __name__ == '__main__':
    Extract().run()
