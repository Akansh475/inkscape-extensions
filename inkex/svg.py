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

import lxml
from lxml import etree

class SvgDocumentElement(etree.ElementBase):
    tag_name = 'svg'

class SvgClassLookup(etree.CustomElementClassLookup):
    """
    We choose what kind of Elements we should return for each element, providing useful
    SVG based API to our extensions system.
    """
    _lookups = []

    def lookup(self, node_type, document, namespace, name):
        """Choose what kind of functionality our element will have"""
        for cls in self.get_lookups():
            if name.lower() == cls.tag_name:
                return cls

    def get_lookups(self):
        """Scan for and cache a list of available classes"""
        if not self._lookups:
            self._lookups = [cls for cls in locals().values() if hasattr(cls, 'tag_name')]
        return self._lookups

svg_parser = lxml.etree.XMLParser(huge_tree=True)
svg_parser.setElementClassLookup(SvgClassLookup())

