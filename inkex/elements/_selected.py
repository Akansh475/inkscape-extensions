# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Martin Owens <doctormo@gmail.com>
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
# Foundation, Inc.,Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
When items or nodes are selected, these structures provide functionality.
"""

from collections import OrderedDict

from ._base import BaseElement

class SelectedElements(OrderedDict):
    """
    A set of selected elements in an svg document.

    Default iterator is always elements (values) not ids
    """
    def __init__(self, svg):
        self.svg = svg
        super().__init__()

    def __iter__(self):
        return self.values().__iter__()

    def ids(self):
        """Return a list of ids in this selection"""
        return list(super().__iter__())

    def set(self, *ids):
        """
        Sets the currently selected elements to these ids, any existing
        selection is cleared.

        Arguments a list of element ids, element objects or
            a single xpath expression starting with "//".

        All element objects must have an id to be correctly set.

        >>> selection.set("rect123", "path456", "text789")
        >>> selection.set(elem1, elem2, elem3)
        >>> selection.set("//rect")
        """
        self.clear()
        self.add(*ids)

    def set_all(self, *types):
        """Select all elements in the svg document"""
        self.set(*list(self.svg.descendants(*types)))

    def pop(self, key=None):
        """Remove the key item or remove the last item selected"""
        if self and key is None:
            key = self.ids()[-1]
        return super().pop(key)

    def add(self, *ids):
        """Like set() but does not clear first"""

        # Allow selecting of xpath elements directly
        if len(ids) == 1 and isinstance(ids[0], str) and ids[0].startswith('//'):
            ids = self.svg.xpath(ids[0])

        for elem_id in ids:
            if isinstance(elem_id, BaseElement):
                # Selection is a list of nodes to select
                self[elem_id.get('id')] = elem_id
                continue
            # Selection is a text element id, find it (or them).
            self[elem_id] = self.svg.getElementById(elem_id)

    def paint_order(self):
        """Get the selected elements, but ordered by their apperence in the document"""
        output = SelectedElements(self.svg)
        ids = self.ids()
        for _id in self.svg.xpath('//@id'):
            if _id in ids:
                output[_id] = self[_id]
        return output

    def get(self, *types):
        """Gets selected nodes of the given type, returns a new SelectedElements object"""
        output = SelectedElements(self.svg)
        for elem_id, node in self.items():
            if not types or isinstance(node, types):
                output[elem_id] = node
        return output

    def bounding_box(self):
        """
        Gets a :class:`inkex.transforms.BoundingBox` object for the selected items.

        Text objects have a bounding box without width or height that only
        reflects the coordinate of their anchor. If a text object is a part of
        the selection's boundary, the bounding box may be inaccurate.

        When no object is selected or when the object's location cannot be
        determined (e.g. empty group or layer), all coordinates will be None.
        """
        return sum([node.bounding_box() for node in self], None)

    def first(self):
        """Returns the first item in the selected list"""
        for node in self:
            return node
        return None
