# -*- coding: utf-8 -*-
#
# Copyright (c) Aaron Spike <aaron@ekips.org>
#               Aurélio A. Heckert <aurium(a)gmail.com>
#               Bulia Byak <buliabyak@users.sf.net>
#               Nicolas Dufour, nicoduf@yahoo.fr
#               Peter J. R. Moulder <pjrm@users.sourceforge.net>
#               Martin Owens <doctormo@gmail.com>
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
# pylint: disable=attribute-defined-outside-init
#
"""
Provide a way to load lxml attributes with an svg API on top.
"""

import random
from collections import OrderedDict

import lxml
from lxml import etree

from .units import discover_unit, convert_unit, render_unit
from .utils import removeNS
from .transforms import BoundingBox
from .elements import ( # pylint: disable=unused-import
    BaseElement, OtherElements, Group, PathElement, Points, Rectangle, Image,
    Circle, Ellipse, TextElement, TextPath, Use, Defs, NamedView, Metadata, Guide, Tspan, Marker
)

class SvgDocumentElement(BaseElement):
    """Provide access to the document level svg functionality"""
    tag_name = 'svg'

    def _init(self):
        self.current_layer = None
        self.view_center = (0.0, 0.0)
        self.selected = OrderedDict()
        self.ids = {}

    def get_ids(self):
        """Returns a set of unique document ids"""
        if not self.ids:
            self.ids = set(self.xpath('//@id'))
        return self.ids

    def get_unique_id(self, old_id):
        """Generate a new id from an existing old_id"""
        ids = self.get_ids()
        while old_id in ids:
            old_id += str(random.randint(0, 9))
        self.ids.add(old_id)
        return old_id

    def set_selected(self, *ids):
        """Sets the currently selected elements to these ids"""
        self.selected = OrderedDict()
        for elem_id in ids:
            if isinstance(elem_id, BaseElement):
                # Selection is a list of nodes to select
                self.selected[elem_id.get('id')] = elem_id
                continue
            # Selection is a text element id, find it (or them).
            for node in self.xpath('//*[@id="{}"]'.format(elem_id)):
                self.selected[elem_id] = node

    def get_z_selected(self):
        """Get the selected elements, but ordered by their apperence in the document"""
        sel = self.selected
        return OrderedDict((_id, sel[_id]) for _id in self.xpath('//@id') if _id in sel)

    def get_selected_bbox(self):
        """Gets the bounding box of the selected items"""
        ret = sum([node.bounding_box() for node in self.selected.values()])
        return BoundingBox(None) if ret == 0 else ret

    def get_current_layer(self):
        """Returns the currently selected layer"""
        layer = self.getElementById(self.namedview.current_layer, 'svg:g')
        if layer is None:
            return self
        return layer

    def get_center_position(self):
        """Returns view_center in terms of document units"""
        namedview = self.namedview
        if namedview.center_x and namedview.center_y:
            return (self.unittouu(namedview.center_x),
                    self.unittouu(namedview.center_y))
            # y-coordinate flip, eliminate it when it's gone in Inkscape
            # doc_height = self.unittouu(self.height)
            # return (float(x), doc_height - float(y))
        return 0.0, 0.0

    # This used to be called Effect.xpathSingle
    def getElement(self, xpath):  # pylint: disable=invalid-name
        """Gets a single element from the given xpath or returns None"""
        el_list = self.xpath(xpath)
        return el_list[0] if el_list else None

    def getElementById(self, eid, elm='*'):  # pylint: disable=invalid-name
        """Get an element in this svg document by it's ID attribute"""
        return self.getElement('//{}[@id="{}"]'.format(elm, eid))

    @property
    def name(self):
        """Returns the Document Name"""
        return self.get('sodipodi:docname', '')

    @property
    def namedview(self):
        """Return the sp namedview meta information element"""
        nvs = self.xpath('//sodipodi:namedview')
        if not nvs:
            # We auto create a namedview element when needed
            nvs = [NamedView()]
            self.insert(0, nvs[0])
        return nvs[0]

    @property
    def defs(self):
        """Return the svg defs meta element container"""
        defs = self.xpath('//svg:defs')
        if not defs:
            defs = [Defs()]
            self.insert(0, defs[0])
        return defs[0]

    def get_viewbox(self):
        """Parse and return the document's viewBox attribute"""
        try:
            ret = [float(unit) for unit in self.get('viewBox', '0').split()]
        except ValueError:
            ret = ''
        if len(ret) != 4:
            return [0, 0, 0, 0]
        return ret

    @property
    def width(self):  # getDocumentWidth(self):
        """Fault tolerance for lazily defined SVG"""
        return self.get('width') or self.get_viewbox()[2] or '0'

    @property
    def height(self):  # getDocumentHeight(self):
        """Returns a string corresponding to the height of the document, as
        defined in the SVG file. If it is not defined, returns the height
        as defined by the viewBox attribute. If viewBox is not defined,
        returns the string '0'."""
        return self.get('height') or self.get_viewbox()[3] or '0'

    @property
    def unit(self):
        """Returns the unit used for in the SVG document.
        In the case the SVG document lacks an attribute that explicitly
        defines what units are used for SVG coordinates, it tries to calculate
        the unit from the SVG width and viewBox attributes.
        Defaults to 'px' units."""
        viewbox = self.get_viewbox()
        if viewbox and set(viewbox) != {0}:
            return discover_unit(self.width, viewbox[2], default='px')
        return 'px'  # Default is px

    def unittouu(self, value):
        """Convert a unit value into the document's units"""
        return convert_unit(value, self.unit)

    def uutounit(self, value, to_unit):
        """Convert from the document's units to the given unit"""
        return convert_unit(render_unit(value, self.unit), to_unit)

    def add_unit(self, value):
        """Add document unit when no unit is specified in the string """
        return render_unit(value, self.unit)


class SvgClassLookup(etree.CustomElementClassLookup):
    """
    We choose what kind of Elements we should return for each element, providing useful
    SVG based API to our extensions system.
    """
    _lookups = []

    def lookup(self, node_type, document, namespace, name):  # pylint: disable=unused-argument
        """Choose what kind of functionality our element will have"""
        for cls in self.get_lookups():
            nsp, tag = removeNS(getattr(cls, 'tag_name', None), True)
            tags = getattr(cls, 'tag_names', [])
            if name in tags:
                return cls
            if name == (tag or '') and \
                    (not namespace or not nsp or nsp == namespace):
                return cls

        import inkex
        inkex.errormsg("Failed to look up element: {}:{} ({})".format(
                node_type, name, namespace))

    def get_lookups(self):
        """Scan for and cache a list of available classes"""
        if not self._lookups:
            self._lookups = set(BaseElement._subclasses())

        return self._lookups


SVG_PARSER = lxml.etree.XMLParser(huge_tree=True)
SVG_PARSER.setElementClassLookup(SvgClassLookup())
