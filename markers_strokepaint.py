#!/usr/bin/env python
# coding=utf-8
# coding=utf-8
#
# Copyright (C) 2006 Aaron Spike, aaron@ekips.org
# Copyright (C) 2010 Nicolas Dufour, nicoduf@yahoo.fr (color options)
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

import copy

import inkex
from inkex.localization import _

class MarkerStrokePaintEffect(inkex.EffectExtension):
    def __init__(self):
        super(MarkerStrokePaintEffect, self).__init__()
        self.arg_parser.add_argument(
                "-m", "--modify", type=inkex.Boolean, dest="modify", default=False,
                help="Do not create a copy, modify the markers")
        self.arg_parser.add_argument(
                "-t", "--type", type=str, dest="fill_type", default="stroke",
                help="Replace the markers' fill with the object stroke or fill color")
        self.arg_parser.add_argument(
                "-a", "--alpha", type=inkex.Boolean, dest="assign_alpha", default=True,
                help="Assign the object fill and stroke alpha to the markers")
        self.arg_parser.add_argument(
                "-i", "--invert", type=inkex.Boolean, default=False,
                help="Invert fill and stroke colors")
        self.arg_parser.add_argument(
                "--assign_fill", type=inkex.Boolean, default=True,
                help="Assign a fill color to the markers")
        self.arg_parser.add_argument(
                "-f", "--fill_color", type=inkex.Color, default=inkex.Color(1364325887),
                help="Choose a custom fill color")
        self.arg_parser.add_argument(
                "--assign_stroke", type=inkex.Boolean, dest="assign_stroke", default=True,
                help="Assign a stroke color to the markers")
        self.arg_parser.add_argument(
                "-s", "--stroke_color", type=inkex.Color, default=inkex.Color(1364325887),
                help="Choose a custom fill color")
        self.arg_parser.add_argument(
                "--tab", type=str, dest="tab", default='"custom"',
                help="The selected UI-tab when OK was pressed")
        self.arg_parser.add_argument(
                "--colortab", type=str, dest="colortab",
                help="The selected custom color tab when OK was pressed")

    def effect(self):
        defs = self.svg.defs

        for id, node in self.svg.selected.items():
            mprops = ['marker', 'marker-start', 'marker-mid', 'marker-end']
            try:
                style = dict(inkex.Style.parse_str(node.get('style')))
            except:
                inkex.errormsg(_("No style attribute found for id: %s") % id)
                continue

            # Use object colors
            if self.options.tab == '"object"':
                temp_stroke = style.get('stroke', '#000000')
                temp_fill = style.get('fill', '#000000')
                if self.options.invert:
                    fill = temp_stroke
                    stroke = temp_fill
                else:
                    fill = temp_fill
                    stroke = temp_stroke
                if self.options.assign_alpha:
                    temp_stroke_opacity = style.get('stroke-opacity', '1')
                    temp_fill_opacity = style.get('fill-opacity', '1')
                    if self.options.invert:
                        fill_opacity = temp_stroke_opacity
                        stroke_opacity = temp_fill_opacity
                    else:
                        fill_opacity = temp_fill_opacity
                        stroke_opacity = temp_stroke_opacity
                if self.options.fill_type == "solid":
                    fill = stroke
                    if self.options.assign_alpha:
                        fill_opacity = stroke_opacity
            # Choose custom colors
            elif self.options.tab == '"custom"':
                fill = str(self.options.fill_color.to_rgb())
                fill_opacity = self.options.fill_color.alpha
                stroke = str(self.options.stroke_color.to_rgb())
                stroke_opacity = self.options.stroke_color.alpha
                if not self.options.assign_fill:
                    fill = "none"
                if not self.options.assign_stroke:
                    stroke = "none"

            for mprop in mprops:
                if mprop in style and style[mprop] != 'none' and style[mprop][:5] == 'url(#':
                    marker_id = style[mprop][5:-1]
                    try:
                        old_mnode = self.svg.getElement('/svg:svg//svg:marker[@id="%s"]' % marker_id)
                        if self.options.modify:
                            mnode = old_mnode
                        else:
                            mnode = copy.deepcopy(old_mnode)
                    except:
                        inkex.errormsg(_("unable to locate marker: %s") % marker_id)
                        continue

                    if self.options.modify:
                        new_id = marker_id
                    else:
                        new_id = self.svg.get_unique_id(marker_id)

                    style[mprop] = "url(#%s)" % new_id
                    mnode.set('id', new_id)
                    mnode.set(inkex.addNS('stockid', 'inkscape'), new_id)
                    if not self.options.modify:
                        defs.append(mnode)

                    children = mnode.xpath('.//*[@style]')
                    for child in children:
                        cstyle = dict(inkex.Style.parse_str(child.get('style')))
                        if not ('stroke' in cstyle and self.options.tab == '"object"' and cstyle['stroke'] == 'none' and self.options.fill_type == "filled"):
                            cstyle['stroke'] = stroke
                            if 'stroke_opacity' in locals():
                                cstyle['stroke-opacity'] = stroke_opacity
                        if not ('fill' in cstyle and self.options.tab == '"object"' and cstyle['fill'] == 'none' and self.options.fill_type == "solid"):
                            cstyle['fill'] = fill
                            if 'fill_opacity' in locals():
                                cstyle['fill-opacity'] = fill_opacity
                        child.set('style', str(inkex.Style(cstyle)))
            node.set('style', str(inkex.Style(style)))


if __name__ == '__main__':
    MarkerStrokePaintEffect().run()
