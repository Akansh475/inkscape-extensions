#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2008 Jonas Termeau - jonas.termeau **AT** gmail.com
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
# Thanks to:
#
# Bernard Gray - bernard.gray **AT** gmail.com (python helping)
# Jamie Heames (english translation issues)
# ~suv (bug report in v2.3)
# http://www.gutenberg.eu.org/publications/ (9x9 margins settings)
#
"""
This basic extension allows you to automatically draw guides in inkscape.
"""

from math import cos, sin, sqrt
import math
from typing import List, Tuple
import re

import inkex

from inkex.localization import inkex_gettext as _


class GuidesOpts:
    """Value storage for Guides Creator"""

    # pylint: disable=too-few-public-methods
    def __init__(self, svg: inkex.SvgDocumentElement) -> None:

        # get page bounds
        self.pages = svg.namedview.get_pages()
        self.viewbox = svg.get_viewbox()
        # in case the viewbox attribute is not set, fall back to viewport
        self.viewbox[2:4] = svg.viewbox_width, svg.viewbox_height
        self.set_page(1)

    def set_page(self, pagenumber):
        """Update guide origin and width/height based on page number (1-indexed)"""
        pagenumber = pagenumber - 1
        if pagenumber < len(self.pages):
            self.page_origin = (self.pages[pagenumber].x, self.pages[pagenumber].y)
            self.width = self.pages[pagenumber].width
            self.height = self.pages[pagenumber].height
        elif pagenumber == 0:  # Single page document
            self.page_origin = (
                self.viewbox[:2]
                if not self.pages
                else (self.pages[0].x, self.pages[0].y)
            )
            self.width = self.viewbox[2]
            self.height = self.viewbox[3]
        else:
            raise ValueError("Invalid page number")

        # getting edges coordinates
        self.orientation = ((round(self.height, 4), 0), (0, round(self.width, 4)))


class GuidesCreator(inkex.EffectExtension):
    """Create a set of guides based on the given options"""

    def add_arguments(self, pars):
        pars.add_argument(
            "--pages",
            type=str,
            help='On which pages the guides are created, e.g. "1, 2, 4-6, 8-". '
            "Default: All pages.",
            default="1-",
        )
        pars.add_argument(
            "--tab",
            type=self.arg_method("generate"),
            default="regular_guides",
            help="Type of guides to create.",
        )
        pars.add_argument("--guides_preset", default="custom", help="Preset")
        pars.add_argument(
            "--vertical_guides", type=int, default=2, help="Vertical guides"
        )
        pars.add_argument(
            "--horizontal_guides", type=int, default=3, help="Horizontal guides"
        )
        pars.add_argument(
            "--start_from_edges", type=inkex.Boolean, help="Start from edges"
        )
        pars.add_argument(
            "--ul", type=inkex.Boolean, default=False, help="Upper left corner"
        )
        pars.add_argument(
            "--ur", type=inkex.Boolean, default=False, help="Upper right corner"
        )
        pars.add_argument(
            "--ll", type=inkex.Boolean, default=False, help="Lower left corner"
        )
        pars.add_argument(
            "--lr", type=inkex.Boolean, default=False, help="Lower right corner"
        )
        pars.add_argument(
            "--margins_preset",
            default="custom",
            choices=[
                "custom",
                "book_left",
                "book_right",
                "book_alternating_right",
                "book_alternating_left",
            ],
            help="Margins preset",
        )
        pars.add_argument("--vert", type=int, default=0, help="Vert subdivisions")
        pars.add_argument("--horz", type=int, default=0, help="Horz subdivisions")
        pars.add_argument(
            "--header_margin", type=int, default="10", help="Header margin"
        )
        pars.add_argument(
            "--footer_margin", type=int, default="10", help="Footer margin"
        )
        pars.add_argument("--left_margin", type=int, default="10", help="Left margin")
        pars.add_argument("--right_margin", type=int, default="10", help="Right margin")
        pars.add_argument("--delete", type=inkex.Boolean, help="Delete existing guides")
        pars.add_argument(
            "--nodup", type=inkex.Boolean, help="Omit duplicated guides", default=True
        )

    def __init__(self):
        super().__init__()
        self.opts: GuidesOpts = None

    @staticmethod
    def parse_page_descriptor(pages, lastpage):
        """Parses a page descriptor. e.g:
        1,2,4-5,7,9- is parsed to 1, 2, 4, 5, 7, 9, 10, ..., lastpage"""
        # replace 4-7 with 4, 5, 6, 7
        pages = re.sub(
            r"(\d+)\s?-\s?(\d+)",
            lambda m: ",".join(map(str, range(int(m.group(1)), int(m.group(2)) + 1))),
            pages,
        )
        # replace 5- with 5, 6, ..., lastpage
        pages = re.sub(
            r"(\d+)\s?-",
            lambda m: ",".join(map(str, range(int(m.group(1)), lastpage + 1))),
            pages,
        )
        pages = map(int, re.findall(r"(\d+)", pages))
        pages = tuple({i for i in pages if i <= lastpage})
        return pages

    def effect(self):

        if self.options.delete:
            for guide in self.svg.namedview.get_guides():
                guide.delete()

        self.opts = GuidesOpts(self.svg)
        for i in self.parse_page_descriptor(
            self.options.pages, max(len(self.svg.namedview.get_pages()), 1)
        ):
            self.opts.set_page(i)
            self.options.tab()

    def generate_regular_guides(self):
        """Generate a regular set of guides"""
        preset = self.options.guides_preset
        from_edges = self.options.start_from_edges
        if preset == "custom":
            h_division = self.options.horizontal_guides
            v_division = self.options.vertical_guides
            if from_edges:
                v_division = v_division or 1
                h_division = h_division or 1

            self.draw_guides(v_division, from_edges, vert=True)
            self.draw_guides(h_division, from_edges, vert=False)

        elif preset == "golden":
            gold = (1 + sqrt(5)) / 2

            for fraction, index in zip([1 / gold, 1 - 1 / gold] * 2, [1, 1, 0, 0]):
                position = fraction * (self.opts.width, self.opts.height)[index]
                self.draw_guide(
                    (0, position) if index == 1 else (position, 0),
                    self.opts.orientation[index],
                )

            if from_edges:

                self.draw_guides(1, True, vert=False)
                self.draw_guides(1, True, vert=True)

        elif ";" in preset:
            v_division = int(preset.split(";")[0])
            h_division = int(preset.split(";")[1])
            self.draw_guides(v_division, from_edges, vert=True)
            self.draw_guides(h_division, from_edges, vert=False)
        else:
            raise inkex.AbortExtension(_("Unknown guide preset: {}").format(preset))

    def generate_diagonal_guides(self):
        """Generate diagonal guides"""
        # Dimentions
        left, bottom = (0, 0)
        right, top = (self.opts.width, self.opts.height)

        # Diagonal angle
        angle = 45

        corner_guides = {
            "ul": ((left, top), (cos(angle), cos(angle))),
            "ur": ((right, top), (-sin(angle), sin(angle))),
            "ll": ((left, bottom), (-cos(angle), cos(angle))),
            "lr": ((right, bottom), (-sin(angle), -sin(angle))),
        }

        for key, (position, orientation) in corner_guides.items():
            if getattr(self.options, key):
                self.draw_guide(position, orientation)

    def generate_margins(self):
        """Generate margin guides"""

        if self.options.start_from_edges:
            # horizontal borders
            self.draw_guide((0, self.opts.height), self.opts.orientation[1])
            self.draw_guide((self.opts.height, 0), self.opts.orientation[1])

            # vertical borders
            self.draw_guide((0, self.opts.width), self.opts.orientation[0])
            self.draw_guide((self.opts.width, 0), self.opts.orientation[0])

        if self.options.margins_preset == "custom":
            margins = [
                (i / j if int(j) != 0 else None)
                for i, j in zip(
                    (
                        self.opts.height * (self.options.header_margin - 1),  # header
                        self.opts.height,  # footer
                        self.opts.width,  # left
                        self.opts.width * (self.options.right_margin - 1),  # right
                    ),
                    (
                        self.options.header_margin,
                        self.options.footer_margin,
                        self.options.left_margin,
                        self.options.right_margin,
                    ),
                )
            ]

        book_options = {
            "book_left": (8 / 9, 2 / 9, 2 / 9, 8 / 9),
            "book_right": (8 / 9, 2 / 9, 1 / 9, 7 / 9),
        }
        if self.options.margins_preset in book_options:
            margins = [
                i * j
                for i, j in zip(
                    book_options[self.options.margins_preset],
                    2 * [self.opts.height] + 2 * [self.opts.width],
                )
            ]

        y_header, y_footer, x_left, x_right = [
            i or j for i, j in zip(margins, [self.opts.height, 0, 0, self.opts.width])
        ]

        for length, position in zip(margins, [1, 1, 0, 0]):
            if length is None:
                continue
            self.draw_guide(
                (length, 0) if position == 0 else (0, length),
                self.opts.orientation[position],
            )

        # setting up properties of the rectangle created between guides
        rectangle_height = y_header - y_footer
        rectangle_width = x_right - x_left

        for subdiv, vert, begin_from in zip(
            (self.options.horz, self.options.vert), (False, True), (y_footer, x_left)
        ):
            if subdiv != 0:
                self._draw_guides(
                    (rectangle_width, rectangle_height),
                    subdiv,
                    edges=0,
                    shift=begin_from,
                    vert=vert,
                )

    def draw_guides(self, division, edges, vert=False):
        """Draw a vertical or horizontal lines"""
        return self._draw_guides(
            (self.opts.width, self.opts.height), division, edges, vert=vert
        )

    def _draw_guides(self, vector, division, edges, shift=0, vert=False):
        if division <= 0:
            return

        # Vert controls both ort template and vector calculation
        def ort(x):
            return (x, 0) if vert else (0, x)

        var = int(bool(edges))
        for x in range(0, division - 1 + 2 * var):
            div = vector[not bool(vert)] / division
            position = round(div + (x - var) * div + shift, 4)
            orientation = round(vector[bool(vert)], 4)
            self.draw_guide(ort(position), ort(orientation))

    def draw_guide(self, position, orientation):
        """Draw the guides"""
        newpos = [
            position[0] + self.opts.page_origin[0],
            position[1]
            + self.opts.viewbox[3]
            - self.opts.height
            - self.opts.page_origin[1],
        ]
        if self.options.nodup:
            self.svg.namedview.new_unique_guide(newpos, orientation)
        else:
            self.svg.namedview.new_guide(newpos, orientation)


if __name__ == "__main__":
    GuidesCreator().run()
