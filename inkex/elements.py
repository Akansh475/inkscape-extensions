# -*- coding: utf-8 -*-
#
# Copyright (c) Martin Owens <doctormo@gmail.com>
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
Provide extra utility to each svg element type specific to it's type.

This is useful for having a common interface for each element which can
give path, transform, and property access easilly.
"""

from lxml import etree

from .transforms import Transform
from .utils import NSS

class BaseElement(etree.ElementBase):
    """Provide automatic namespaces to all calls"""
    def xpath(self, pattern, namespaces=NSS): # pylint: disable=dangerous-default-value
        """Wrap xpath call and add svg namespaces"""
        return super(BaseElement, self).xpath(pattern, namespaces=namespaces)

    def findall(self, pattern, namespaces=NSS): # pylint: disable=dangerous-default-value
        """Wrap findall call and add svg namespaces"""
        return super(BaseElement, self).findall(pattern, namespaces=namespaces)

    root = property(lambda self: self.getparent().root if self.getparent() else self)
    transform = property(lambda self: Transform(self.get('transform', None)))
    transform.setter(lambda self, matrix: self.set('transform', str(Transform(matrix))))

    def composed_transform(self):
        """Calculate every transform down to the root document node"""
        if self.getparent():
            return self.transform * self.getparent().composed_transform()
        return self.transform


class Group(BaseElement):
    """Any group element (layer or regular group)"""
    tag_name = 'g'


class Path(BaseElement):
    """Provide a useful extension for path elements"""
    tag_name = 'path'
    path = property(lambda self: self.get('d'))

class Points(BaseElement):
    """Provide a useful extension for points elements"""
    tag_name = 'points'
    path = property(lambda self: 'M' + self.get('points'))

class Rectangle(BaseElement):
    """Provide a useful extension for rectangle elements"""
    tag_name = 'rect'
    left = property(lambda self: float(self.get('x', '0')))
    top = property(lambda self: float(self.get('y', '0')))
    width = property(lambda self: float(self.get('width')))
    height = property(lambda self: float(self.get('height')))

    @property
    def path(self):
        """Calculate the path as the box around the rect"""
        return 'M {.left},{.top} h{.width}v{.height}h-{.width}'.format(self)


class Image(Rectangle):
    """Provide a useful extension for image elements"""
    tag_name = 'image'


class Circle(BaseElement):
    """Provide a useful extension for circle elements"""
    tag_name = 'circle'
    radius = property(lambda self: self.get('r'))
    radius_x = property(lambda self: float(self.get('rx', self.radius)))
    radius_y = property(lambda self: float(self.get('ry', self.radius)))
    center_x = property(lambda self: float(self.get('cx', '0')))
    center_y = property(lambda self: float(self.get('cy', '0')))
    left = property(lambda self: self.center_x - self.radius_x)
    right = property(lambda self: self.center_x + self.radius_x)

    @property
    def path(self):
        """Calculte the arc path of this circle/elipse"""
        return ('M {.left} {.right} '\
                'A {.radius_x},{.radius_y} 0 1 0 {.right}, {.center_y} '\
                'A {.radius_x},{.radius_y} 0 1 0 {.left}, {.center_y}').format(self)


class Ellipse(Circle):
    """Provide a similar extension to the Circle interface"""
    tag_name = 'ellipse'


class Use(BaseElement):
    """A 'use' element that links to another in the document"""
    tag_name = 'use'

    path = property(lambda self: self.ref.path)

    def ref(self):
        """Returns the reffered to element if available"""
        return self.root.getElementById(self.get('href'))

