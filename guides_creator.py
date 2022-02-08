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

import inkex
from inkex import Guide

from inkex.localization import inkex_gettext as _


class GuidesOpts:
    """Value storage for Guides Creator"""

    # pylint: disable=too-few-public-methods
    def __init__(self, svg) -> None:
        self.width = svg.viewbox_width
        self.height = svg.viewbox_height

        # getting edges coordinates
        self.h_orientation = (0, round(self.width, 4))
        self.v_orientation = (round(self.height, 4), 0)


class GuidesCreator(inkex.EffectExtension):
    """Create a set of guides based on the given options"""

    def add_arguments(self, pars):
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
            choices=["custom", "book_left", "book_right"],
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

    def __init__(self):
        super().__init__()
        self.opts: GuidesOpts = None

    def effect(self):
        self.opts = GuidesOpts(self.svg)

        if self.options.delete:
            for guide in self.svg.namedview.get_guides():
                guide.delete()

        return self.options.tab()

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
                    (self.opts.v_orientation, self.opts.h_orientation)[index],
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
            "ul": ((top, left), (cos(angle), cos(angle))),
            "ur": ((right, top), (-sin(angle), sin(angle))),
            "ll": ((bottom, left), (-cos(angle), cos(angle))),
            "lr": ((bottom, right), (-sin(angle), -sin(angle))),
        }

        for key, (position, orientation) in corner_guides.items():
            if getattr(self.options, key):
                self.draw_guide(position, orientation)

    def generate_margins(self):
        """Generate margin guides"""

        if self.options.start_from_edges:
            # horizontal borders
            self.draw_guide((0, self.opts.height), self.opts.h_orientation)
            self.draw_guide((self.opts.height, 0), self.opts.h_orientation)

            # vertical borders
            self.draw_guide((0, self.opts.width), self.opts.v_orientation)
            self.draw_guide((self.opts.width, 0), self.opts.v_orientation)

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
                (self.opts.v_orientation, self.opts.h_orientation)[position],
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
        """Create a guide directly into the namedview"""
        if isinstance(position, tuple):
            x, y = position
        self.svg.namedview.add(Guide().move_to(float(x), float(y), orientation))


if __name__ == "__main__":
    GuidesCreator().run()
