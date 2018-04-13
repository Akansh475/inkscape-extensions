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
"""
Provide a way to load lxml attributes with an svg API on top.
"""

import sys
import math
import inspect
import random
import lxml
from lxml import etree

from .units import discover_unit, convert_unit, render_unit

# a dictionary of all of the xmlns prefixes in a standard inkscape doc
NSS = {
    u'sodipodi' :u'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    u'cc'       :u'http://creativecommons.org/ns#',
    u'ccOLD'    :u'http://web.resource.org/cc/',
    u'svg'      :u'http://www.w3.org/2000/svg',
    u'dc'       :u'http://purl.org/dc/elements/1.1/',
    u'rdf'      :u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    u'inkscape' :u'http://www.inkscape.org/namespaces/inkscape',
    u'xlink'    :u'http://www.w3.org/1999/xlink',
    u'xml'      :u'http://www.w3.org/XML/1998/namespace'
}

def addNS(tag, ns=None): # pylint: disable=invalid-name
    """Add a known namespace to a name for use with lxml"""
    if ns is not None and len(ns) > 0 and ns in NSS and len(tag) > 0 and tag[0] != '{':
        return "{%s}%s" % (NSS[ns], tag)
    return tag


class SvgDocumentElement(etree.ElementBase):
    """Provide access to the document level svg functionality"""
    tag_name = 'svg'
    def __init__(self, *args, **kw):
        super(SvgDocumentElement, self).__init__(*args, **kw)
        self.selected = {}
        self.ids = {}

    def get_ids(self):
        """Returns a set of unqiue document ids"""
        if not self.ids:
            self.ids = set(self.xpath('//@id', namespaces=NSS))
        return self.ids

    def get_unique_id(self, old_id):
        """Generate a new id from an existing old_id"""
        ids = self.get_ids()
        while old_id in ids:
            old_id += random.randint(0, 9)
        return old_id

    def set_selected(self, *ids):
        """Sets the currently selected elements to these ids"""
        self.selected = {}
        for elem_id in ids:
            for node in self.xpath('//*[@id="{}"]'.format(elem_id), namespaces=NSS):
                self.selected[elem_id] = node

    def get_posinlayer(self):
        """defines view_center in terms of document units"""
        self.current_layer = self
        self.view_center = (0.0, 0.0)

        layerattr = self.xpath('//sodipodi:namedview/@inkscape:current-layer', namespaces=NSS)
        if layerattr:
            self.current_layer = self.getElementById(layerattr[0], 'svg:g')

        xattr = self.xpath('//sodipodi:namedview/@inkscape:cx', namespaces=NSS)
        yattr = self.xpath('//sodipodi:namedview/@inkscape:cy', namespaces=NSS)
        if xattr and yattr:
            x = self.unittouu(xattr[0] + 'px')
            y = self.unittouu(yattr[0] + 'px')
            doc_height = self.unittouu(self.height)
            if x and y:
                # FIXME: y-coordinate flip, eliminate it when it's gone in Inkscape
                self.view_center = (float(x), doc_height - float(y))

    def getElement(self, xpath): # pylint: disable=invalid-name
        """Gets a single element from the given xpath or returns None"""
        # XXX This used to be called Effect.xpathSingle
        el_list = self.xpath(xpath, namespaces=NSS)
        return el_list[0] if el_list else None

    def getElementById(self, eid, elm='*'): # pylint: disable=invalid-name
        """Get an element in this svg document by it's ID attribute"""
        return self.getElement('//{}[@id="{}"]'.format(elm, eid))

    def getNamedView(self):
        """Return the sp namedview meta information element"""
        # TODO: We should make one if it doesn't exist...
        return self.xpath('//sodipodi:namedview', namespaces=NSS)[0]

    def getViewBox(self):
        """Parse and return the document's viewBox attribute"""
        return [float(unit) for unit in self.get('viewBox', '0 0 0 0').split()]

    @property
    def width(self): #getDocumentWidth(self):
        """Fault tolerance for lazily defined SVG"""
        return self.get('width') or self.getViewBox()[2] or '0'

    @property
    def height(self): #getDocumentHeight(self):
        """Returns a string corresponding to the height of the document, as
        defined in the SVG file. If it is not defined, returns the height
        as defined by the viewBox attribute. If viewBox is not defined,
        returns the string '0'."""
        return self.get('height') or self.getViewBox()[3] or '0'

    def getDocumentUnit(self):
        """Returns the unit used for in the SVG document.
        In the case the SVG document lacks an attribute that explicitly
        defines what units are used for SVG coordinates, it tries to calculate
        the unit from the SVG width and viewBox attributes.
        Defaults to 'px' units."""
        viewbox = self.getViewBox()
        if viewbox and set(viewbox) != {0}:
            return discover_unit(self.width, viewbox[2], default='px')
        return 'px' # Default is px

    def unittouu(self, value):
        """Convert a unit value into the document's units"""
        return convert_unit(value, self.getDocumentUnit())

    def uutounit(self, value, to_unit):
        """Convert from the document's units to the given unit"""
        return convert_unit(render_unit(value, self.getDocumentUnit()), to_unit)

    def addDocumentUnit(self, value):
        """Add document unit when no unit is specified in the string """
        return render_unit(value, self.getDocumentUnit())


class NamedViewElement(etree.ElementBase):
    """The NamedView element is Inkscape specific metadata about the file"""
    tag_name = 'namedview'

    def create_guide(self, pos_x, pos_y, angle):
        """Create a guide in this namedView section"""
        atts = {
            'position': str(pos_x)+','+str(pos_y),
            'orientation': "{},{}".format(
                str(math.sin(math.radians(angle))),
                str(-math.cos(math.radians(angle)))
            ),
        }
        return etree.SubElement(self, addNS('guide', 'sodipodi'), atts)


class SvgClassLookup(etree.CustomElementClassLookup):
    """
    We choose what kind of Elements we should return for each element, providing useful
    SVG based API to our extensions system.
    """
    _lookups = []

    def lookup(self, node_type, document, namespace, name): # pylint: disable=unused-argument
        """Choose what kind of functionality our element will have"""
        for cls in self.get_lookups():
            if name.lower() == cls.tag_name:
                return cls

    def get_lookups(self):
        """Scan for and cache a list of available classes"""
        if not self._lookups:
            module = sys.modules[__name__]
            self._lookups = [
                cls for _, cls in inspect.getmembers(module) \
                  if inspect.isclass(cls) and issubclass(cls, etree.ElementBase)
            ]
        return self._lookups

SVG_PARSER = lxml.etree.XMLParser(huge_tree=True)
SVG_PARSER.setElementClassLookup(SvgClassLookup())

