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

import inkex
from inkex.elements import (
    Rectangle, FlowRoot, FlowPara, FlowRegion, TextElement, Tspan
)

class Merge(inkex.Effect):
    def __init__(self):
        super(Merge, self).__init__()
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
                                     type=inkex.inkbool,
                                     dest="flowtext", default=False,
                                     help="use a flow text structure instead of a normal text element")
        self.arg_parser.add_argument("-k", "--keepstyle",
                                     type=inkex.inkbool,
                                     dest="keepstyle", default=False,
                                     help="keep format")

    def effect(self):
        if not self.svg.selected:
            for node in self.svg.xpath('//svg:text | //svg:flowRoot'):
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
                text_element = FlowRoot
                text_span = FlowPara
            else:
                text_element = TextElement
                text_span = Tspan

            text_root = parentnode.add(text_element())
            text_root.set('xml:space', 'preserve')
            text_root.style = {
                'font-size': '20px',
                'font-style': 'normal',
                'font-weight': 'normal',
                'line-height': '125%',
                'letter-spacing': '0px',
                'word-spacing': '0px',
                'fill': '#000000',
                'fill-opacity': 1,
                'stroke': 'none'
            }

            for _, node in objlist:
                self.recurse(text_span, node, text_root)

            if self.options.flowtext:
                region = text_root.add(FlowRegion())
                region.set('xml:space', 'preserve')
                rect = region.add(Rectangle())
                rect.set('xml:space', 'preserve')
                rect.set('height', 200)
                rect.set('width', 200)

    def recurse(self, text_span, node, span):
        if not isinstance(node, FlowRegion):

            newspan = span.add(text_span())
            newspan.set('xml:space', 'preserve')

            newspan.set('sodipodi:role', node.get('sodipodi:role'))
            if isinstance(node, (TextElement, FlowPara)):
                newspan.set('sodipodi:role', 'line')

            if self.options.keepstyle:
                newspan.style = node.style

            if node.text is not None:
                newspan.text = node.text
            for child in node:
                self.recurse(text_span, child, newspan)
            if node.tail and not isinstance(node, TextElement):
                newspan.tail = node.tail


if __name__ == '__main__':
    Merge().run()
