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
    WRAPPED_ATTRS = {
        'transform': Transform,
        'style': Style,
    }

    @classmethod
    def _subclasses(cls):
        """Get subclasses, recursively
        @rtype generator
        """
        for subcls in cls.__subclasses__():
            yield subcls
            for subsubcls in subcls._subclasses():
                yield subsubcls

    def __getattr__(self, name):
        """Get the attribute, but load it if it's not available yet"""
        if name in self.WRAPPED_ATTRS:
            # The reason we do this here and not in _init is because lxml
            # is inconsistant about when elements are initialised.
            # So we make this a lazy property.
            def _set_attr(new_item):
                if new_item:
                    self.set(name, str(new_item))
                else:
                    self.attrib.pop(name, None)

            value = self.WRAPPED_ATTRS[name](self.attrib.get(name, None), callback=_set_attr)
            setattr(self, name, value)
            return value
        raise AttributeError("Can't find attribute {}".format(name))

    def __setattr__(self, name, value):
        """Set the attribute, update the attrib if needed"""
        if name in self.WRAPPED_ATTRS:
            # Don't call hasattr or getattr (infinate loop)
            if name in self.__dict__:
                del self.__dict__[name].callback
            # Don't call self.set or self.get (infinate loop)
            if value:
                self.attrib[name] = str(value)
            else:
                self.attrib.pop(name, None)
            if name in self.__dict__:
                delattr(self, name)
        else:
            super(BaseElement, self).__setattr__(name, value)

    def get(self, name, default=None):
        """Get element attribute named, with addNS support."""
        if name in self.WRAPPED_ATTRS:
            value = getattr(self, name, None)
            # We check the boolean nature of the value, because empty
            # transformations and style attributes are equiv to not-existing
            ret = str(value) if value else (default or None)
            return ret
        return super(BaseElement, self).get(addNS(name), default)

    def set(self, name, value):
        """Set element attribute named, with addNS support."""
        if name in self.WRAPPED_ATTRS:
            # Always keep the local wrapped class up to date.
            setattr(self, name, self.WRAPPED_ATTRS[name](value))
            value = str(getattr(self, name))
            if not value:
                return
        return super(BaseElement, self).set(addNS(name), value)

    @property
    def path(self):
        """Gets the outline or path of the element, this can be a simple bounding box for most"""
        return Path(self.get_path())

    @path.setter
    def path(self, path):
        self.set_path(path)

    def get_path(self):
        raise NotImplementedError("Path should be provided by svg element {}."
                                  .format(type(self).__name__))

    def set_path(self):
        raise NotImplementedError("Path should be set by svg element {}."
                                  .format(type(self).__name__))

    def xpath(self, pattern, namespaces=NSS):  # pylint: disable=dangerous-default-value
        """Wrap xpath call and add svg namespaces"""
        return super(BaseElement, self).xpath(pattern, namespaces=namespaces)

    def findall(self, pattern, namespaces=NSS):  # pylint: disable=dangerous-default-value
        """Wrap findall call and add svg namespaces"""
        return super(BaseElement, self).findall(pattern, namespaces=namespaces)

    @property
    def root(self):
        """Get the root document element from any element descendent"""
        if self.getparent() is not None:
            return self.getparent().root
        return self

    def composed_transform(self):
        """Calculate every transform down to the root document node"""
        if self.getparent() is not None:
            return self.transform * self.getparent().composed_transform()
        return self.transform

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
        x, y = self.bounding_box().center()
        return x or 0, y or 0

    def decendants(self):
        """Walks the element tree and yields all elements, parent first"""
        yield self
        for child in self:
            for decendant in child.decendants():
                yield decendant

    @property
    def label(self):
        """Returns the inkscape label"""
        return self.get('inkscape:label', None)

    def __str__(self):
        # We would do more here, but lxml is VERY unpleseant when it comes to
        # namespaces, basically over printing details and providing no
        # supression mechanisms to turn off xml's over engineering.
        return str(self.tag).split('}')[-1]


class OtherElements(BaseElement):
    """A bunch of other svg elements"""
    tag_names = [
        'desc',
        'fegaussianblur',
        'filter',
        'flowPara',
        'flowRegion',
        'flowRoot',
        'font',
        'font-face',
        'format',
        'rdf',
        'type',
        'work',
        'style',
    ]

    def bounding_box(self):
        """Other elements have no bounding box"""
        return BoundingBox(None)


class Group(BaseElement):
    """Any group element (layer or regular group)"""
    tag_name = 'g'
    is_layer = lambda self: self.groupmode == 'layer'

    def bounding_box(self):
        bbox = BoundingBox(None)
        for child in self:
            bbox += child.bounding_box()
        return bbox

    @property
    def groupmode(self):
        """Return the type of group this is"""
        return self.get('inkscape:groupmode', 'group')

class Anchor(Group):
    """An anchor or link tag"""
    tag_name = 'a'

class PathElement(BaseElement):
    """Provide a useful extension for path elements"""
    tag_name = 'path'
    get_path = lambda self: self.get('d')

    def set_path(self, path):
        """Set the given data as a path as the 'd' attribute"""
        self.set('d', str(Path(path)))

    def apply_transform(self):
        """Apply the internal transformation to this node and delete"""
        if 'transform' in self.attrib:
            self.path.transform(self.transform)
            self.set('d', str(self.path))
            self.set('transform', Transform())

    @property
    def original_path(self):
        """Returns the original path if this is an LPE, or the path if not"""
        return Path(self.get('inkscape:original-d', self.path))

    @original_path.setter
    def original_path(self, path):
        if addNS('inkscape:original-d') in self.attrib:
            self.set('inkscape:original-d', str(Path(path)))
        else:
            self.path = path

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

class ClipPath(BaseElement):
    """A path used to clip objects"""
    tag_name = 'clipPath'

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

class ForeignObject(BaseElement):
    """SVG foreignObject element"""
    tag_name = 'foreignObject'

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

class Switch(BaseElement):
    """A switch element"""
    tag_name = 'switch'

class Grid(BaseElement):
    """A namedview grid child"""
    tag_name = 'inkscape:grid'

class Script(BaseElement):
    """A javascript tag in SVG"""
    tag_name = 'script'
