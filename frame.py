#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2016 Richard White, rwhite8282@gmail.com
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
An Inkscape extension that creates a frame around a selected object.
"""
import copy

import inkex
from inkex.utils import inkbool
from inkex.elements import Group, PathElement, ClipPath
from inkex.generic import GenerateExtension

def color_in(value):
    """ Returns color data in style string format.
    value -- The value returned from the color picker.
    Returns an object with color and opacity properties.
    """
    val = '{:08X}'.format(int(value) & 0xFFFFFFFF)
    color = '#' + val[0:-2].rjust(6, '0')
    opacity = '{:1.2f}'.format(float(int(val[6:].rjust(2, '0'), 16)) / 255)
    return type('', (object,), {'color': color, 'opacity': opacity})()


def size_box(box, delta):
    """ Returns a box with an altered size.
    delta -- The amount the box should grow.
    Returns a box with an altered size.
    """
    return (box[0] - delta), (box[1] + delta), (box[2] - delta), (box[3] + delta)


# Frame maker Inkscape effect extension
class Frame(GenerateExtension):
    """ An Inkscape extension that creates a frame around a selected object.
    """

    def __init__(self):
        super(Frame, self).__init__()
        self.defs = None

        # Parse the options.
        self.arg_parser.add_argument('--clip', type=inkbool, dest='clip', default=False)
        self.arg_parser.add_argument('--corner_radius', type=int, dest='corner_radius', default=0)
        self.arg_parser.add_argument('--fill_color', type=color_in, default=color_in(0))
        self.arg_parser.add_argument('--group', type=inkbool, dest='group', default=False)
        self.arg_parser.add_argument('--position', type=str, dest='position', default='outside')
        self.arg_parser.add_argument('--stroke_color', type=color_in, default=color_in(0))
        self.arg_parser.add_argument('--tab', type=str, dest='tab', default='object')
        self.arg_parser.add_argument('--width', type=float, dest='width', default=2.0)

    def add_clip(self, node, clip_path):
        """ Adds a new clip path node to the defs and sets
                the clip-path on the node.
            node -- The node that will be clipped.
            clip_path -- The clip path object.
        """
        clip = ClipPath()
        clip.append(PathElement(d=str(clip_path.path)))
        clip_id = self.svg.get_unique_id('clipPath')
        clip.set('id', clip_id)
        self.svg.defs.append(clip)
        node.set('clip-path', 'url(#{})'.format(str(clip_id)))

    def add_frame(self, name, box, style, radius=0):
        """
            name -- The name of the new frame object.
            box -- The boundary box of the node.
            style -- The style used to draw the path.
            radius -- The corner radius of the frame.
            returns a new frame node.
        """
        r = min([radius, (abs(box[1] - box[0]) / 2), (abs(box[3] - box[2]) / 2)])
        if radius > 0:
            d = ' '.join(str(x) for x in
                         ['M', box[0], (box[2] + r),
                          'A', r, r, '0 0 1', (box[0] + r), box[2],
                          'L', (box[1] - r), box[2],
                          'A', r, r, '0 0 1', box[1], (box[2] + r),
                          'L', box[1], (box[3] - r),
                          'A', r, r, '0 0 1', (box[1] - r), box[3],
                          'L', (box[0] + r), box[3],
                          'A', r, r, '0 0 1', box[0], (box[3] - r),
                          'Z'])
        else:
            d = ' '.join(str(x) for x in
                         ['M', box[0], box[2],
                          'L', box[1], box[2],
                          'L', box[1], box[3],
                          'L', box[0], box[3],
                          'Z'])

        attributes = {'style': style, inkex.addNS('label', 'inkscape'): name, 'd': d}
        return PathElement(**attributes)

    def generate(self):
        """Performs the effect."""
        # Get the style values.
        corner_radius = self.options.corner_radius
        stroke_data = self.options.stroke_color
        fill_data = self.options.fill_color

        # Determine common properties.
        position = self.options.position
        width = self.options.width
        style = str(inkex.Style({'stroke': stroke_data.color,
                                 'stroke-opacity': stroke_data.opacity,
                                 'stroke-width': str(width),
                                 'fill': (fill_data.color or 'none'),
                                 'fill-opacity': fill_data.opacity}))

        for node in self.svg.selected.values():
            box = node.bounding_box()
            if position == 'outside':
                box = size_box(box, (width / 2))
            else:
                box = size_box(box, -(width / 2))

            frame = self.add_frame("Frame", box, style, corner_radius)
            if self.options.clip:
                self.add_clip(node, frame)
            if self.options.group:
                group = Group()
                group.append(node)
                group.append(frame)
                yield group
            else:
                yield frame


if __name__ == '__main__':
    Frame().run()
