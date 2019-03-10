# -*- coding: utf-8 -*-
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
Provide extra utility to each svg element type specific to it's type.

This is useful for having a common interface for each element which can
give path, transform, and property access easily.
"""

import math

from lxml import etree

from .paths import Path
from .styles import Style
from .transforms import BoundingBox
from .transforms import Transform
from .utils import NSS, addNS, removeNS


class BaseElement(etree.ElementBase):
    """Provide automatic namespaces to all calls"""
    tag_name = 'none'
    TAG = property(lambda self: removeNS(self.tag_name)[-1])
    NAMESPACE = property(lambda self: removeNS(self.tag_name, url=True)[0])

    @property
    def path(self):
        """Gets the outline or path of the element, this can be a simple bounding box for most"""
        return Path(self.get_path())

    def get_path(self):
        raise NotImplementedError("Path should be provided by svg element {}."
                                  .format(type(self).__name__))

    def xpath(self, pattern, namespaces=NSS):  # pylint: disable=dangerous-default-value
        """Wrap xpath call and add svg namespaces"""
        return super(BaseElement, self).xpath(pattern, namespaces=namespaces)

    def findall(self, pattern, namespaces=NSS):  # pylint: disable=dangerous-default-value
        """Wrap findall call and add svg namespaces"""
        return super(BaseElement, self).findall(pattern, namespaces=namespaces)

    def get(self, name, default=None):
        """Get element attribute named, with addNS support."""
        return super(BaseElement, self).get(addNS(name), default)

    def set(self, name, value):
        """Set element attribute named, with addNS support."""
        return super(BaseElement, self).set(addNS(name), value)

    @property
    def root(self):
        """Get the root document element from any element descendent"""
        if self.getparent() is not None:
            return self.getparent().root
        return self

    transform = property(lambda self: Transform(self.get('transform', None)),
                         lambda self, matrix: self.set('transform', str(Transform(matrix))))

    def composed_transform(self):
        """Calculate every transform down to the root document node"""
        if self.getparent() is not None:
            return self.transform * self.getparent().composed_transform()
        return self.transform

    style = property(lambda self: Style(self.get('style', None)))

    def composed_style(self):
        """Calculate the final styles applied to this element"""
        # FUTURE: We could compose styles from class/css too.
        if self.getparent() is not None:
            return self.getparent().composed_style() + self.style
        return self.style

    def bounding_box(self):
        """Returns the bounding box for the element as a BoundingBox object (x1, x2, y1, y2)"""
        return self.path.bounding_box()

    def get_center_position(self):
        """Returns object's center in terms of document units"""
        return self.bounding_box().center()

    def __str__(self):
        # We would do more here, but lxml is VERY unpleseant when it comes to
        # namespaces, basically over printing details and providing no
        # supression mechanisms to turn off xml's over engineering.
        return str(self.tag).split('}')[-1]


class OtherElements(BaseElement):
    """A bunch of other svg elements"""
    tag_names = ['work', 'rdf', 'format', 'type', 'desc', 'font', 'font-face', 'filter', 'fegaussianblur']


class Group(BaseElement):
    """Any group element (layer or regular group)"""
    tag_name = 'g'

    def bounding_box(self):
        bbox = BoundingBox(None)
        for child in self:
            bbox += child.bounding_box()
        return bbox


class PathElement(BaseElement):
    """Provide a useful extension for path elements"""
    tag_name = 'path'
    get_path = lambda self: self.get('d')


class Points(BaseElement):
    """Provide a useful extension for points elements"""
    tag_name = 'points'
    get_path = lambda self: 'M' + self.get('points')


class Rectangle(BaseElement):
    """Provide a useful extension for rectangle elements"""
    tag_name = 'rect'
    left = property(lambda self: float(self.get('x', '0')))
    top = property(lambda self: float(self.get('y', '0')))
    width = property(lambda self: float(self.get('width')))
    height = property(lambda self: float(self.get('height')))

    def get_path(self):
        """Calculate the path as the box around the rect"""
        return 'M {0.left},{0.top} h{0.width}v{0.height}h-{0.width}'.format(self)


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

    def get_path(self):
        """Calculte the arc path of this circle/elipse"""
        return ('M {0.left} {0.right} '
                'A {0.radius_x},{0.radius_y} 0 1 0 {0.right}, {0.center_y} '
                'A {0.radius_x},{0.radius_y} 0 1 0 {0.left}, {0.center_y}'
                ).format(self)


class Ellipse(Circle):
    """Provide a similar extension to the Circle interface"""
    tag_name = 'ellipse'


class Use(BaseElement):
    """A 'use' element that links to another in the document"""
    tag_name = 'use'

    path = property(lambda self: self.ref().path)  # pylint: disable=no-member

    def ref(self):
        """Returns the referred to element if available"""
        return self.root.getElementById(self.get('xlink:href').strip('#'))


class Defs(BaseElement):
    """An header defs element, one per document"""
    tag_name = 'defs'


class NamedView(BaseElement):
    """The NamedView element is Inkscape specific metadata about the file"""
    tag_name = 'sodipodi:namedview'

    center_x = property(lambda self: self.get('inkscape:cx'))
    center_y = property(lambda self: self.get('inkscape:cy'))
    current_layer = property(lambda self: self.get('inkscape:current-layer'))

    def get_guides(self):
        """Returns a list of guides"""
        return self.findall('sodipodi:guide')

    def create_guide(self, pos_x, pos_y, angle):
        """Create a guide in this namedView section"""
        self.append(Guide(pos_x, pos_y, angle))


class Guide(BaseElement):
    """An inkscape guide"""
    tag_name = 'sodipodi:guide'

    def __init__(self, *args):
        super(Guide, self).__init__()
        if args:
            self.move_to(*args)

    def move_to(self, pos_x, pos_y, angle=None):
        """Move this guide to the given position"""
        self.set('position', "{:g},{:g}".format(pos_x, pos_y))
        if angle is not None:
            self.set('orientation', "{:g},{:g}".format(
                    math.sin(math.radians(angle)),
                    -math.cos(math.radians(angle))
            ))


class Metadata(BaseElement):
    """Inkscape Metadata element"""
    tag_name = 'metadata'


class TextElement(BaseElement):
    """A Text element"""
    tag_name = 'text'

    def bounding_box(self):
        """TODO"""
        return BoundingBox(None)


class TextPath(BaseElement):
    """A textPath element"""
    tag_name = 'textPath'

    def append_superscript(self, text):
        """Adds a superscript tspan element"""
        self.append(Tspan(text, style="font-size:65%;baseline-shift:super"))


class Tspan(BaseElement):
    """A tspan text element"""
    tag_name = 'tspan'


class Marker(BaseElement):
    """The <marker> element defines the graphic that is to be used for drawing arrowheads
     or polymarkers on a given <path>, <line>, <polyline> or <polygon> element."""
    tag_name = 'marker'
