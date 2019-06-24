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

import os
import sys
import types

from lxml.etree import fromstring

from .utils import errormsg
from .elements import SVG_PARSER, BaseElement, Group
from .base import InkscapeExtension, SvgThroughMixin, SvgInputMixin, SvgOutputMixin, TempDirMixin
from .transforms import TranslateTransform

# All the names that get added to the inkex API itself.
__all__ = ('EffectExtension', 'GenerateExtension', 'InputExtension', 'OutputExtension', 'CallExtension')

stdout = sys.stdout
if sys.version_info[0] == 3:  #PY3
    unicode = str  # pylint: disable=redefined-builtin,invalid-name

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

class CallExtension(TempDirMixin, InputExtension):
    """Call an external program to get the output"""
    input_ext = 'svg'
    output_ext = 'svg'

    def load(self, stream):
        pass # Not called (load_raw instead)

    def load_raw(self):
        # Don't call InputExtension.load_raw
        TempDirMixin.load_raw(self)
        input_file = self.options.input_file

        if not isinstance(input_file, (unicode, str)):
            data = input_file.read()
            input_file = os.path.join(self.tempdir, 'input.' + self.input_ext)
            with open(input_file, 'wb') as fhl:
                fhl.write(data)

        output_file = os.path.join(self.tempdir, 'output.' + self.output_ext)
        document = self.call(input_file, output_file) or output_file
        if isinstance(document, (str, unicode)):
            if not os.path.isfile(document):
                raise IOError("Can't find generated document: {}".format(document))

            if self.output_ext == 'svg':
                with open(document, 'r') as fhl:
                    document = fhl.read()
                if '<' in document:
                    document = fromstring(document, parser=SVG_PARSER)
            else:
                with open(document, 'rb') as fhl:
                    document = fhl.read()

        self.document = document

    def call(self, input_file, output_file):
        """Call whatever programs are needed to get the desired result."""
        raise NotImplementedError("Call extensions require a call(in, out) method!")

class GenerateExtension(EffectExtension):
    """
    Does not need any SVG, but instead just outputs an SVG fragment which is
    inserted into Inkscape, centered on the selection.
    """
    container_label = ''
    container_layer = False

    def generate(self):
        """
        Return an SVG fragment to be inserted into the selected layer of the document
        OR yield multiple elements which will be grouped into a container Group
        element which will be given an automatic label and transformation.
        """
        raise NotImplementedError("Generate extensions must provide generate()")

    def container_transform(self):
        """
        Generate the transformation for the container group, the default is
        to return the center position of the svg document or view port.
        """
        (pos_x, pos_y) = self.svg.get_center_position()
        if pos_x is None:
            pos_x = 0
        if pos_y is None:
            pos_y = 0
        return TranslateTransform(pos_x, pos_y)

    def effect(self):
        layer = self.svg.get_current_layer()
        fragment = self.generate()
        if isinstance(fragment, types.GeneratorType):
            container = Group.create(self.container_label, self.container_layer)
            if self.container_layer:
                self.svg.append(container)
            else:
                container.transform = self.container_transform()
                layer.append(container)
            for child in fragment:
                if isinstance(child, BaseElement):
                    container.append(child)
        elif isinstance(fragment, BaseElement):
            layer.append(fragment)
        else:
            errormsg("Nothing was generated\n")
