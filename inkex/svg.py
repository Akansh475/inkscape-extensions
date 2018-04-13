#
# Copyright (c) 2018 - Martin Owens <doctormo@gmail.com>
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
import inspect
import lxml
from lxml import etree

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
            # TODO: Fix this up
            old_id = re.sub(r'\d+', random.digits())
        return old_id

    def set_selected(self, *ids):
        """Sets the currently selected elements to these ids"""
        self.selected = {}
        for elem_id in ids:
            for node in self.xpath('//*[@id="{}"]'.format(elem_id), namespaces=NSS):
                self.selected[elem_id] = node


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

