#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2007-2019 Matt Harrison, matthewharrison [at] gmail.com
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
A script that slices images.  It might be useful for web design.

You pass it the name of a layer containing rectangles that cover
the areas that you want exported (the default name for this layer
is "slices").  It then sets the opacity to 0 for all the rectangles
defined in that layer and exports as png whatever they covered.
The output filenames are based on the "Id" field of "Object Properties"
right click contextual menu of the rectangles.

One side effect is that after exporting, it sets the slice rectangles
to different colors with a 25% opacity.  (If you want to hide them,
just click on the eye next to the layer).

  * red - overwrote a file
  * green - wrote a new file
  * grey - skipped (not overwriting)

For good pixel exports set the Document Properties, default units to "px"
and the width/height to the real size. (I use 1024x768)

Here's the process I've used for slicing web layout with
Inkscape: Create your webpage layout (set page units to "px",
width/height appropriately and snap to 1 pixel intervals. This should
allow pixel perfect alignment). Then create a new layer, naming it
slices. Draw rectangles over the areas you want to slice (set
x,y,width,height to whole pixel values). Name these rectangles using
the Object Properties found in the right click contextual menu (the
saved images name will be based on that value, so name them something
like "header" instead of the default/non-useful "rect4312"). 

"""
import os
import sys
import tempfile

import inkex
from inkex.command import inkscape


class ExportSlices(inkex.EffectExtension):
    """Exports all rectangles in the current layer"""
    GREEN = "#00ff00"  # new export
    GREY = "#555555"   # not exported
    RED = "#ff0000"    # overwrite


    def __init__(self):
        super(ExportSlices, self).__init__()
        self.color_map = {}  # map node id to color based on overwrite


    def add_arguments(self, pars):
        pars.add_argument(
            "-d",
            "--directory",
            dest="directory",
            default=os.path.expanduser("~"),
            help="Existing destination directory",
        )
        pars.add_argument(
            "-l",
            "--layer",
            dest="layer_name",
            default="slices",
            help="Layer with slices (rects) in it",
        )
        pars.add_argument(
            "-i",
            "--iconmode",
            type=inkex.Boolean,
            default=False,
            help="Icon export mode",
        )
        pars.add_argument(
            "-s",
            "--sizes",
            dest="sizes",
            default="128, 64, 48, 32, 24, 16",
            help="sizes to export comma separated",
        )
        pars.add_argument(
            "-o",
            "--overwrite",
            type=inkex.Boolean,
            default=False,
            help="Overwrite existing exports?",
        )
        pars.add_argument(
            "--dpi",
            dest="dpi",
            default="300",
            help="Dots per inch (300 default)",
        )


    def effect(self):
        if not os.path.isdir(self.options.directory):
            os.makedirs(self.options.directory)

        nodes = self.get_layer_nodes(self.options.layer_name)
        if nodes is None:
            inkex.errormsg(
                "Slice layer: '{}' does not exist.".format(
                    self.options.layer_name
                )
            )
            return

        # set opacity to zero in slices
        for node in nodes:
            self.clear_color(node)

        # in case there are overlapping rects, clear them all out before
        # saving any
        for node in nodes:
            if self.options.iconmode:
                for s in self.options.sizes.split(","):
                    s = s.strip()
                    if s.isdigit():
                        png_size = int(s)
                        self.export_node(node, png_size, png_size)
            else:
                self.export_node(node)

        # change slice colors to grey/green/red and set opacity to 25% in real document
        for node in nodes:
            self.change_color(node)


    def get_layer_nodes(self, layer_name):
        """
        given the name of a layer one that contains the rectangles defining slices,
        return the nodes of the rectangles.
        """
        # get layer we intend to slice
        document = self.document
        slice_node = None
        slice_layer = document.findall(inkex.addNS('g', 'svg'))
        for node in slice_layer:
            label_value = node.label 
            if label_value == layer_name:
                slice_node = node

        if slice_node is not None:
            return slice_node.findall(inkex.addNS('rect', "svg"))
        return slice_node


    def clear_color(self, node):
        """
        set opacity to zero, and stroke to none

        Node looks like this:
        <rect
        style="opacity:0;fill:#eeeeec;fill-opacity:1;stroke:none;stroke-width:4.00099993;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;display:inline"
        """
        node.style.update({"stroke": "none", "opacity": "0"})


    def change_color(self, node):
        """
        set color from color_map and set opacity to 25%
        
        """
        node_id = node.attrib["id"]
        color = self.color_map[node_id]
        node.style.update({"fill": color, "opacity": ".25"})


    def export_node(self, node, height=None, width=None):
        color, kwargs = self.get_color_and_command_kwargs(node, height, width)
        node_id = kwargs['export-id']
        self.color_map[node_id] = color
        if color == ExportSlices.GREY:  # skipping
            return
        svg_file = self.options.input_file 
        inkscape(svg_file, **kwargs)
        

    def get_color_and_command_kwargs(self, node, height=None, width=None):
        directory = self.options.directory
        node_id = node.attrib['id']
        size = '' if height is None else '-{}x{}'.format(width, height)
        file_name = "{}{}.png".format(node_id, size)
        filename = os.path.join(directory, file_name)
        color = ExportSlices.GREY  # skipping
        if self.options.overwrite or not os.path.exists(filename):
            color = ExportSlices.RED  #  overwritten
            if not os.path.exists(filename):
                color = ExportSlices.GREEN  # new export
            kwargs = {'export-id': node_id, 'export-file': filename,
                      'export-dpi': self.options.dpi}
            if width:
                kwargs['export-height'] = str(height)
                kwargs['export-width'] = str(width)
            return color, kwargs
        else:
            inkex.errormsg("Export exists ({}) not overwriting".format(filename))
            return color, {}

if __name__ == "__main__":
    ExportSlices().run()
