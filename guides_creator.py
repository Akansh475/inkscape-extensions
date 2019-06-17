#!/usr/bin/env python
# coding=utf-8
#
# Guides Creator v2.31 (05/07/2009)
# http://code.google.com/p/inkscape-guides-creator/
#
# Copyright (C) 2008 Jonas Termeau - jonas.termeau **AT** gmail.com
#
# Thanks to:
#
# Bernard Gray - bernard.gray **AT** gmail.com (python helping)
# Jamie Heames (english translation issues)
# ~suv (bug report in v2.3)
# http://www.gutenberg.eu.org/publications/ (9x9 margins settings)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
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
"""
This basic extension allows you to automatically draw guides in inkscape.
"""

# Inspired by hello_world turorial by Blackhex and Rubikcube
# (http://wiki.inkscape.org/wiki/index.php/PythonEffectTutorial)

# Making an .INX file : http://wiki.inkscape.org/wiki/index.php/MakingAnINX
# see also http://codespeak.net/lxml/dev/tutorial.html#namespaces for XML namespaces manipulation

# # # # # # # #
# TODO:  See http://code.google.com/p/inkscape-guides-creator/wiki/Roadmap
# # # # # # # #


from math import cos, sin, sqrt

from lxml import etree

import inkex
from inkex import inkbool
from inkex.generic import EffectExtension

def drawVerticalGuides(division, w, h, edges, parent, vertical_shift=0):
    if division > 0:
        if edges:
            var = 1
        else:
            var = 0

    for v in range(0, division - 1 + 2 * var):
        # setting up the guide's attributes (id is generated automatically)
        position = str(round((w / division) + (v - var) * (w / division) + vertical_shift, 4)) + ",0"
        orientation = str(round(h, 4)) + ",0"
        createGuide(position, orientation, parent)


def drawHorizontalGuides(division, w, h, edges, parent, horizontal_shift=0):
    if division > 0:
        if edges:
            var = 1
        else:
            var = 0

        for x in range(0, division - 1 + 2 * var):
            # setting up the guide's attributes (id is generated automatically)
            position = "0," + str(round((h / division) + (x - var) * (h / division) + horizontal_shift, 4))
            orientation = "0," + str(round(w, 4))
            createGuide(position, orientation, parent)


def createGuide(position, orientation, parent):
    # Create a sodipodi:guide node
    # (look into inkex's namespaces to find 'sodipodi' value in order to make a "sodipodi:guide" tag)
    # see NSS array in file inkex.py for the other namespaces
    etree.SubElement(parent, '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide', {'position': position, 'orientation': orientation})


def getVerticalDivisionsFromPreset(preset):
    # take a "string1;string2" preset
    # and return "string1"
    str_array = preset.split(';')
    return int(str_array[0])


def getHorizontalDivisionsFromPreset(preset):
    # take a "string1;string2" preset
    # and return "string2"
    str_array = preset.split(';')
    result = int(str_array[1])
    return result


def deleteAllGuides(document):
    for guide in document.getroot().get_guides():
        guide.delete()

class GuidesCreator(EffectExtension):
    def __init__(self):
        """Defines options of the script."""
        super(GuidesCreator, self).__init__()

        # Define option for the tab.
        self.arg_parser.add_argument("--tab",
                                     type=str,
                                     dest="tab", default="regular_guides",
                                     help="")

        # Define string option "--preset" with default value 'custom'.
        self.arg_parser.add_argument('--guides_preset',
                                     type=str,
                                     dest='guides_preset', default='custom',
                                     help='Preset')

        # Define string option "--vertical_guides" with default value '0'.
        self.arg_parser.add_argument('--vertical_guides',
                                     type=str,
                                     dest='vertical_guides', default=0,
                                     help='Vertical guides each:')

        # Define string option "--horizontal_guides" with default value '0'.
        self.arg_parser.add_argument('--horizontal_guides',
                                     type=str,
                                     dest='horizontal_guides', default=0,
                                     help='Horizontal guides each:')

        # Define boolean option "--start_from_edges" with default value False.
        self.arg_parser.add_argument('--start_from_edges',
                                     type=inkbool,
                                     dest='start_from_edges', default=False,
                                     help='Start from edges')

        # Define boolean option "--delete_existing_guides" with default value False.
        self.arg_parser.add_argument('--delete_existing_guides',
                                     type=inkbool,
                                     dest='delete_existing_guides', default=False,
                                     help='Delete existing guides')

        # Define boolean option "--upper_left_corner" with default value False.
        self.arg_parser.add_argument('--ul',
                                     type=inkbool,
                                     dest='ul', default=False,
                                     help='Upper left corner')

        # Define boolean option "--upper_right_corner" with default value False.
        self.arg_parser.add_argument('--ur',
                                     type=inkbool,
                                     dest='ur', default=False,
                                     help='Upper right corner')

        # Define boolean option "--lower_left_corner" with default value False.
        self.arg_parser.add_argument('--ll',
                                     type=inkbool,
                                     dest='ll', default=False,
                                     help='Lower left corner')

        # Define boolean option "--upper_left_corner" with default value False.
        self.arg_parser.add_argument('--lr',
                                     type=inkbool,
                                     dest='lr', default=False,
                                     help='Lower right corner')

        # Define boolean option "--delete_existing_guides2" with default value False.
        self.arg_parser.add_argument('--delete_existing_guides2',
                                     type=inkbool,
                                     dest='delete_existing_guides2', default=False,
                                     help='Delete existing guides')

        # Define string option "--margins_preset" with default value 'custom'.
        self.arg_parser.add_argument('--margins_preset',
                                     type=str,
                                     dest='margins_preset', default='custom',
                                     help='Margins preset')

        # Define boolean option "--delete_existing_guides3" with default value False.
        self.arg_parser.add_argument('--delete_existing_guides3',
                                     type=inkbool,
                                     dest='delete_existing_guides3', default=False,
                                     help='Delete existing guides')

        # Define string option "--vertical_subdivisions" with default value '0'.
        self.arg_parser.add_argument('--vertical_subdivisions',
                                     type=str,
                                     dest='vertical_subdivisions', default=0,
                                     help='Vertical subdivisions')

        # Define string option "--horizontal_subdivisions" with default value '0'.
        self.arg_parser.add_argument('--horizontal_subdivisions',
                                     type=str,
                                     dest='horizontal_subdivisions', default=0,
                                     help='Horizontal subdivisions')

        # Define string option "--header_margin" with default value '6'.
        self.arg_parser.add_argument('--header_margin',
                                     type=str,
                                     dest='header_margin', default=6,
                                     help='Header margin')

        # Define string option "--footer_margin" with default value '6'.
        self.arg_parser.add_argument('--footer_margin',
                                     type=str,
                                     dest='footer_margin', default=6,
                                     help='Footer margin')

        # Define string option "--left_margin" with default value '6'.
        self.arg_parser.add_argument('--left_margin',
                                     type=str,
                                     dest='left_margin', default=6,
                                     help='Left margin')

        # Define string option "--right_margin" with default value '6'.
        self.arg_parser.add_argument('--right_margin',
                                     type=str,
                                     dest='right_margin', default=6,
                                     help='Right margin')

        # Define boolean option "--start_from_edges2" with default value False.
        self.arg_parser.add_argument('--start_from_edges2',
                                     type=inkbool,
                                     dest='start_from_edges2', default=False,
                                     help='Start from edges')

    def effect(self):
        # Get script's options value.
        tab = self.options.tab

        # first tab
        guides_preset = self.options.guides_preset
        h_division = int(self.options.horizontal_guides)
        v_division = int(self.options.vertical_guides)
        from_edges = self.options.start_from_edges
        delete_existing = self.options.delete_existing_guides

        # second tab
        upper_left = self.options.ul
        upper_right = self.options.ur
        lower_left = self.options.ll
        lower_right = self.options.lr
        delete_existing2 = self.options.delete_existing_guides2

        # third tab
        margins_preset = self.options.margins_preset
        header_margin = int(self.options.header_margin)
        footer_margin = int(self.options.footer_margin)
        left_margin = int(self.options.left_margin)
        right_margin = int(self.options.right_margin)
        h_subdiv = int(self.options.horizontal_subdivisions)
        v_subdiv = int(self.options.vertical_subdivisions)
        from_edges2 = self.options.start_from_edges2
        delete_existing3 = self.options.delete_existing_guides3

        # getting the main SVG document element (canvas)
        svg = self.document.getroot()

        # getting the width and height attributes of the canvas
        width = self.svg.unittouu(svg.get('width'))
        height = self.svg.unittouu(svg.get('height'))

        # getting edges coordinates
        h_orientation = '0,' + str(round(width, 4))
        v_orientation = str(round(height, 4)) + ',0'

        # getting parent tag of the guides
        nv = self.document.find(inkex.addNS('namedview', 'sodipodi'))

        if tab == "\"regular_guides\"":
            if delete_existing:
                deleteAllGuides(self.document)

            if guides_preset == 'custom':
                if (v_division == 0) and from_edges:
                    v_division = 1

                if (h_division == 0) and from_edges:
                    h_division = 1

                # creating vertical guides
                drawVerticalGuides(v_division, width, height, from_edges, nv)

                # creating horizontal guides
                drawHorizontalGuides(h_division, width, height, from_edges, nv)

            elif guides_preset == 'golden':
                gold = (1 + sqrt(5)) / 2

                # horizontal golden guides
                position1 = '0,' + str(height / gold)
                position2 = '0,' + str(height - (height / gold))

                createGuide(position1, h_orientation, nv)
                createGuide(position2, h_orientation, nv)

                # vertical golden guides
                position1 = str(width / gold) + ',0'
                position2 = str(width - (width / gold)) + ',0'

                createGuide(position1, v_orientation, nv)
                createGuide(position2, v_orientation, nv)

                if from_edges:
                    # horizontal borders
                    createGuide('0,' + str(height), h_orientation, nv)
                    createGuide(str(height) + ',0', h_orientation, nv)

                    # vertical borders
                    createGuide('0,' + str(width), v_orientation, nv)
                    createGuide(str(width) + ',0', v_orientation, nv)

            else:
                v_division = getVerticalDivisionsFromPreset(guides_preset)
                h_division = getHorizontalDivisionsFromPreset(guides_preset)
                drawVerticalGuides(v_division, width, height, from_edges, nv)
                drawHorizontalGuides(h_division, width, height, from_edges, nv)

        elif tab == "\"diagonal_guides\"":
            if delete_existing2:
                deleteAllGuides(self.document)

            # diagonal
            angle = 45

            # X axe
            left = 0
            right = width

            # Y axe
            down = 0
            up = height

            ul_corner = str(up) + ',' + str(left)
            ur_corner = str(right) + ',' + str(up)
            ll_corner = str(down) + ',' + str(left)
            lr_corner = str(down) + ',' + str(right)

            from_ul_to_lr = str(cos(angle)) + ',' + str(cos(angle))
            from_ur_to_ll = str(-sin(angle)) + ',' + str(sin(angle))
            from_ll_to_ur = str(-cos(angle)) + ',' + str(cos(angle))
            from_lr_to_ul = str(-sin(angle)) + ',' + str(-sin(angle))

            if upper_left:
                createGuide(ul_corner, from_ul_to_lr, nv)
            if upper_right:
                createGuide(ur_corner, from_ur_to_ll, nv)
            if lower_left:
                createGuide(ll_corner, from_ll_to_ur, nv)
            if lower_right:
                createGuide(lr_corner, from_lr_to_ul, nv)

        elif tab == "\"margins\"":
            if delete_existing3:
                deleteAllGuides(self.document)

            if from_edges2:
                # horizontal borders
                createGuide('0,' + str(height), h_orientation, nv)
                createGuide(str(height) + ',0', h_orientation, nv)

                # vertical borders
                createGuide('0,' + str(width), v_orientation, nv)
                createGuide(str(width) + ',0', v_orientation, nv)

            if margins_preset == 'custom':
                y_header = height
                y_footer = 0
                x_left = 0
                x_right = width

                if header_margin != 0:
                    y_header = (height / header_margin) * (header_margin - 1)
                    createGuide('0,' + str(y_header), h_orientation, nv)

                if footer_margin != 0:
                    y_footer = height / footer_margin
                    createGuide('0,' + str(y_footer), h_orientation, nv)

                if left_margin != 0:
                    x_left = width / left_margin
                    createGuide(str(x_left) + ',0', v_orientation, nv)

                if right_margin != 0:
                    x_right = (width / right_margin) * (right_margin - 1)
                    createGuide(str(x_right) + ',0', v_orientation, nv)

            elif margins_preset == 'book_left':
                # 1/9th header
                y_header = (height / 9) * 8
                createGuide('0,' + str(y_header), h_orientation, nv)

                # 2/9th footer
                y_footer = (height / 9) * 2
                createGuide('0,' + str(y_footer), h_orientation, nv)

                # 2/9th left margin
                x_left = (width / 9) * 2
                createGuide(str(x_left) + ',0', v_orientation, nv)

                # 1/9th right margin
                x_right = (width / 9) * 8
                createGuide(str(x_right) + ',0', v_orientation, nv)

            elif margins_preset == 'book_right':
                # 1/9th header
                y_header = (height / 9) * 8
                createGuide('0,' + str(y_header), h_orientation, nv)

                # 2/9th footer
                y_footer = (height / 9) * 2
                createGuide('0,' + str(y_footer), h_orientation, nv)

                # 2/9th left margin
                x_left = (width / 9)
                createGuide(str(x_left) + ',0', v_orientation, nv)

                # 1/9th right margin
                x_right = (width / 9) * 7
                createGuide(str(x_right) + ',0', v_orientation, nv)

            # setting up properties of the rectangle created between guides
            rectangle_height = y_header - y_footer
            rectangle_width = x_right - x_left

            if h_subdiv != 0:
                begin_from = y_footer

                # creating horizontal guides
                drawHorizontalGuides(h_subdiv, rectangle_width, rectangle_height, 0, nv, begin_from)

            if v_subdiv != 0:
                begin_from = x_left

                # creating vertical guides
                drawVerticalGuides(v_subdiv, rectangle_width, rectangle_height, 0, nv, begin_from)


if __name__ == '__main__':
    GuidesCreator().run()
