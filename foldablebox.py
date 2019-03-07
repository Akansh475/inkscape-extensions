#! /usr/bin/env python
#
# Copyright (C) 2009 Aurelio A. Heckert <aurium (a) gmail dot com>
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

__version__ = "0.2"

from math import *

import inkex
from inkex import inkbool


class FoldableBox(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("-x", "--width",
                         type=float,
                        dest="width", default=10.0,
                        help="The Box Width - in the X dimension")
        self.arg_parser.add_argument("-y", "--height",
                         type=float,
                        dest="height", default=15.0,
                        help="The Box Height - in the Y dimension")
        self.arg_parser.add_argument("-z", "--depth",
                         type=float,
                        dest="depth", default=3.0,
                        help="The Box Depth - in the Z dimension")
        self.arg_parser.add_argument("-u", "--unit",
                         type=str,
                        dest="unit", default="cm",
                        help="The unit of the box dimensions")
        self.arg_parser.add_argument("-p", "--paper-thickness",
                         type=float,
                        dest="thickness", default=0.01,
                        help="Paper Thickness - sometimes that is important")
        self.arg_parser.add_argument("-t", "--tab-proportion",
                         type=float,
                        dest="tabProportion", default=0.6,
                        help="Inner tab proportion for upper tab")
        self.arg_parser.add_argument("-g", "--guide-line",
                         type=inkbool,
                        dest="guideLine", default=True,
                        help="Add guide lines to help the drawing limits")

    def effect(self):

        docW = self.svg.unittouu(self.document.getroot().get('width'))
        docH = self.svg.unittouu(self.document.getroot().get('height'))

        boxW = self.svg.unittouu( str(self.options.width)  + self.options.unit )
        boxH = self.svg.unittouu( str(self.options.height) + self.options.unit )
        boxD = self.svg.unittouu( str(self.options.depth)  + self.options.unit )
        tabProp = self.options.tabProportion
        tabH = boxD * tabProp

        box_id = self.svg.get_unique_id('box')
        self.box = g = inkex.etree.SubElement(self.svg.get_current_layer(), 'g', {'id':box_id})

        line_style = str(inkex.Style({ 'stroke': '#000000', 'fill': 'none', 'stroke-width': str(self.svg.unittouu('1px')) }))

        #self.createGuide( 0, docH, 0 );

        # Inner Close Tab
        line_path = [
                      [ 'M', [ boxW-(tabH*0.7),  0 ] ],
                      [ 'C', [ boxW-(tabH*0.25), 0, boxW, tabH*0.3, boxW, tabH*0.9 ] ],
                      [ 'L', [ boxW, tabH     ] ],
                      [ 'L', [ 0,    tabH     ] ],
                      [ 'L', [ 0,    tabH*0.9 ] ],
                      [ 'C', [ 0,    tabH*0.3, tabH*0.25, 0, tabH*0.7, 0 ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-inner-close-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        lower_pos = boxD+tabH
        left_pos = 0

        #self.createGuide( 0, docH-tabH, 0 );

        # Upper Close Tab
        line_path = [
                      [ 'M', [ left_pos,        tabH      ] ],
                      [ 'L', [ left_pos + boxW, tabH      ] ],
                      [ 'L', [ left_pos + boxW, lower_pos ] ],
                      [ 'L', [ left_pos + 0,    lower_pos ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-upper-close-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxW

        # Upper Right Tab
        sideTabH = lower_pos - (boxW/2)
        if sideTabH < tabH: sideTabH = tabH
        line_path = [
                      [ 'M', [ left_pos,        sideTabH  ] ],
                      [ 'L', [ left_pos + (boxD*0.8), sideTabH  ] ],
                      [ 'L', [ left_pos + boxD, ((lower_pos*3)-sideTabH)/3 ] ],
                      [ 'L', [ left_pos + boxD, lower_pos ] ],
                      [ 'L', [ left_pos + 0,    lower_pos ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-upper-right-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxW + boxD

        # Upper Left Tab
        line_path = [
                      [ 'M', [ left_pos + boxD,       sideTabH  ] ],
                      [ 'L', [ left_pos + (boxD*0.2), sideTabH  ] ],
                      [ 'L', [ left_pos, ((lower_pos*3)-sideTabH)/3 ] ],
                      [ 'L', [ left_pos,              lower_pos ] ],
                      [ 'L', [ left_pos + boxD,       lower_pos ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-upper-left-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos = 0

        #self.createGuide( 0, docH-tabH-boxD, 0 );

        # Right Tab
        line_path = [
                      [ 'M', [ left_pos,            lower_pos                   ] ],
                      [ 'L', [ left_pos - (boxD/2), lower_pos + (boxD/4)        ] ],
                      [ 'L', [ left_pos - (boxD/2), lower_pos + boxH - (boxD/4) ] ],
                      [ 'L', [ left_pos,            lower_pos + boxH            ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-left-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        # Front
        line_path = [
                      [ 'M', [ left_pos,        lower_pos        ] ],
                      [ 'L', [ left_pos + boxW, lower_pos        ] ],
                      [ 'L', [ left_pos + boxW, lower_pos + boxH ] ],
                      [ 'L', [ left_pos,        lower_pos + boxH ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-front', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxW

        # Right
        line_path = [
                      [ 'M', [ left_pos,        lower_pos        ] ],
                      [ 'L', [ left_pos + boxD, lower_pos        ] ],
                      [ 'L', [ left_pos + boxD, lower_pos + boxH ] ],
                      [ 'L', [ left_pos,        lower_pos + boxH ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-right', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxD

        # Back
        line_path = [
                      [ 'M', [ left_pos,        lower_pos        ] ],
                      [ 'L', [ left_pos + boxW, lower_pos        ] ],
                      [ 'L', [ left_pos + boxW, lower_pos + boxH ] ],
                      [ 'L', [ left_pos,        lower_pos + boxH ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-back', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxW

        # Left
        line_path = [
                      [ 'M', [ left_pos,        lower_pos        ] ],
                      [ 'L', [ left_pos + boxD, lower_pos        ] ],
                      [ 'L', [ left_pos + boxD, lower_pos + boxH ] ],
                      [ 'L', [ left_pos,        lower_pos + boxH ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-left', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        lower_pos += boxH
        left_pos = 0
        bTab = lower_pos + boxD
        if bTab > boxW / 2.5: bTab = boxW / 2.5

        # Bottom Front Tab
        line_path = [
                      [ 'M', [ left_pos,        lower_pos            ] ],
                      [ 'L', [ left_pos,        lower_pos + (boxD/2) ] ],
                      [ 'L', [ left_pos + boxW, lower_pos + (boxD/2) ] ],
                      [ 'L', [ left_pos + boxW, lower_pos            ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-bottom-front-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxW

        # Bottom Right Tab
        line_path = [
                      [ 'M', [ left_pos,        lower_pos        ] ],
                      [ 'L', [ left_pos,        lower_pos + bTab ] ],
                      [ 'L', [ left_pos + boxD, lower_pos + bTab ] ],
                      [ 'L', [ left_pos + boxD, lower_pos        ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-bottom-right-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxD

        # Bottom Back Tab
        line_path = [
                      [ 'M', [ left_pos,        lower_pos            ] ],
                      [ 'L', [ left_pos,        lower_pos + (boxD/2) ] ],
                      [ 'L', [ left_pos + boxW, lower_pos + (boxD/2) ] ],
                      [ 'L', [ left_pos + boxW, lower_pos            ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-bottom-back-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxW

        # Bottom Left Tab
        line_path = [
                      [ 'M', [ left_pos,        lower_pos        ] ],
                      [ 'L', [ left_pos,        lower_pos + bTab ] ],
                      [ 'L', [ left_pos + boxD, lower_pos + bTab ] ],
                      [ 'L', [ left_pos + boxD, lower_pos        ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-bottom-left-tab', 'd':str(inkex.Path(line_path)) }
        inkex.etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        left_pos += boxD
        lower_pos += bTab

        g.set( 'transform', 'translate(%f,%f)' % ( (docW-left_pos)/2, (docH-lower_pos)/2 ) )

if __name__ == '__main__':   #pragma: no cover
    FoldableBox().run()

