#!/usr/bin/env python
#
# Copyright (C) 2007-2011 Rob Antonishen; rob.antonishen@gmail.com
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

#import csv
import math
#import os
import random
#from subprocess import PIPE, Popen

import inkex
from inkex.svg import SvgDocumentElement
from inkex.generic import EffectExtension
from inkex.localize import _


class Restack(EffectExtension):
    def __init__(self):
        super(Restack, self).__init__()
        self.arg_parser.add_argument("-d", "--direction",
                                     type=str,
                                     dest="direction", default="tb",
                                     help="direction to restack")
        self.arg_parser.add_argument("-a", "--angle",
                                     type=float,
                                     dest="angle", default=0.0,
                                     help="arbitrary angle")
        self.arg_parser.add_argument("-x", "--xanchor",
                                     type=str,
                                     dest="xanchor", default="m",
                                     help="horizontal point to compare")
        self.arg_parser.add_argument("-y", "--yanchor",
                                     type=str,
                                     dest="yanchor", default="m",
                                     help="vertical point to compare")
        self.arg_parser.add_argument("--zsort",
                                     type=str,
                                     dest="zsort", default="rev",
                                     help="Restack mode based on Z-Order")
        self.arg_parser.add_argument("--tab",
                                     type=str, default='z_order',
                                     dest="tab",
                                     help="The selected UI-tab when OK was pressed")
        self.arg_parser.add_argument("--nb_direction",
                                     type=str, default='',
                                     dest="nb_direction",
                                     help="The selected UI-tab when OK was pressed")

    def effect(self):
        if not self.svg.selected:
            return inkex.errormsg(_("There is no selection to restack."))

        # process selection to get list of objects to be arranged
        parentnode = None
        for node in self.svg.selected.values():
            if isinstance(node, SvgDocumentElement):
                parentnode = node
                self.svg.set_selection(*list(node))

        if parentnode is None:
            parentnode = self.svg.get_current_layer()

        if 'positional' in self.options.tab:
            return self.restack_positional(parentnode)
        elif 'z_order' in self.options.tab:
            return self.restack_z_order(parentnode)

    def restack_positional(self, parentnode):
        objlist = []

        if 'custom' in self.options.nb_direction:
            self.options.direction = "aa"

        # calculate distances for each selected object
        for node in self.svg.selected.values():
            # get the bounding box
            #x, y, w, h = dimen[key]
            bbox = node.bounding_box()

            # calc the comparison coords
            if self.options.xanchor == "l":
                cx = bbox.x.minimum
            elif self.options.xanchor == "r":
                cx = bbox.x.maximum
            else:  # middle
                cx = bbox.x.center

            if self.options.yanchor == "t":
                cy = bbox.y.minimum
            elif self.options.yanchor == "b":
                cy = bbox.y.maximum
            else:  # middle
                cy = bbox.y.center

            # direction chosen
            if self.options.direction == "tb" or (self.options.direction == "aa" and self.options.angle == 270):
                objlist.append([cy, node])
            elif self.options.direction == "bt" or (self.options.direction == "aa" and self.options.angle == 90):
                objlist.append([-cy, node])
            elif self.options.direction == "lr" or (self.options.direction == "aa" and (self.options.angle == 0 or self.options.angle == 360)):
                objlist.append([cx, node])
            elif self.options.direction == "rl" or (self.options.direction == "aa" and self.options.angle == 180):
                objlist.append([-cx, node])
            elif self.options.direction == "aa":
                distance = math.hypot(cx, cy) * (math.cos(math.radians(-self.options.angle) - math.atan2(cy, cx)))
                objlist.append([distance, node])
            elif self.options.direction == "ro":
                selbox = self.svg.get_selected_bbox()
                distance = math.hypot(selbox.x.center - cx, selbox.y.center - cy)
                objlist.append([distance, node])
            elif self.options.direction == "ri":
                distance = -math.hypot(selbox.x.center - cx, selbox.y.center - cy)
                objlist.append([distance, node])

        objlist.sort()
        # move them to the top of the object stack in this order.
        for _, node in objlist:
            parentnode.append(node)
        return True

    def restack_z_order(self, parentnode):
        objects = list(self.svg.selected.values())
        if self.options.zsort == "rev":
            objects.reverse()
        elif self.options.zsort == "rand":
            random.shuffle(objects)
        if parentnode is not None:
            for item in objects:
                parentnode.append(item)
        return True


if __name__ == '__main__':
    Restack().run()
