# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Martin Owens <doctormo@gmail.com>
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
Useful utilities specifically for elements (that aren't base classes)
"""

class ChildToProperty(property):
    """Use when you have a singleton child element who's text
       content is the canonical value for the property"""
    def __init__(self, tag, prepend=False):
        self.tag = tag
        self.prepend = prepend

    def __get__(self, obj, klass=None):
        elem = self.findone(self.tag)
        return elem.text if elem else None

    def __set__(self, obj, value):
        elem = obj.get_or_create(self.tag, prepend=self.prepend)
        elem.text = value

    def __delete__(self, obj):
        obj.remove_all(self.tag)

    @property
    def __doc__(self):
        return f"Get, set or delete the {self.tag} property."
