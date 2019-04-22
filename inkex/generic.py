# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Martin Owens <doctormo@gmail.com>
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
"""
A helper module for creating Inkscape effect extensions

This provides the basic generic types of extensions which most writers should
use in their code. See below for the different types.
"""

import types

from .utils import errormsg
from .elements import BaseElement, Group
from .base import InkscapeExtension, SvgThroughMixin, SvgInputMixin, SvgOutputMixin
from .transforms import TranslateTransform
from .deprecated import DeprecatedEffect

class Effect(SvgThroughMixin, DeprecatedEffect, InkscapeExtension):
    """An Inkscape effect, takes SVG in and outputs SVG"""
    pass

class EffectExtension(SvgThroughMixin, InkscapeExtension):
    """
    Takes the SVG from Inkscape, modifies the selection or the document
    and returns an SVG to Inkscape.
    """
    pass

class OutputExtension(SvgInputMixin, InkscapeExtension):
    """
    Takes the SVG from Inkscape and outputs it to something that's not an SVG.

    Used in functions for `Save As`
    """
    def effect(self):
        """Effect isn't needed for a lot of Output extensions"""
        pass

    def save(self, stream):
        """But save certainly is, we give a more exact message here"""
        raise NotImplementedError("Output extensions require a save(stream) method!")

class InputExtension(SvgOutputMixin, InkscapeExtension):
    """
    Takes any type of file as input and outputs SVG which Inkscape can read.

    Used in functions for `Open`
    """
    def effect(self):
        """Effect isn't needed for a lot of Input extensions"""
        pass

    def load(self, stream):
        """But load certainly is, we give a more exact message here"""
        raise NotImplementedError("Input extensions require a load(stream) method!")

class GenerateExtension(EffectExtension):
    """
    Does not need any SVG, but instead just outputs an SVG fragment which is
    inserted into Inkscape, centered on the selection.
    """
    def generate(self):
        """Return an SVG fragment to be inserted into Inkscape"""
        raise NotImplementedError("Generate extensions must provide generate()")

    def effect(self):

        layer = self.svg.get_current_layer()
        (pos_x, pos_y) = self.svg.get_center_position()
        if pos_x is None:
            pos_x = 0
        if pos_y is None:
            pos_y = 0
        fragment = self.generate()
        if isinstance(fragment, types.GeneratorType):
            container = Group(transform=str(TranslateTransform(pos_x, pos_y)))
            layer.append(container)
            for child in fragment:
                container.append(child)
        elif isinstance(fragment, BaseElement):
            layer.append(fragment)
        else:
            errormsg("Nothing was generated\n")
