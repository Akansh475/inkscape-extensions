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
    WRAPPED_ATTRS = (
        ('transform', Transform),
        ('style', Style),
    )

    # We do this because python2 and python3 have different ways
    # of combining two dictionaries that are incompatible.
    # This allows us to update these with inheritance.
    wrapped_attrs = property(lambda self: dict(self.WRAPPED_ATTRS))

    def __init__(self, *children, **kwargs):
        newkw = {'nsmap': kwargs.pop('nsmap', None)}
        super(BaseElement, self).__init__(*children, **newkw)
        # We covert the setting of all attributes so that we can
        # better control them, both namespaces and value types.
        for key, value in kwargs.pop('attrib', {}).items():
            self.set(key, value)
        for key, value in kwargs.items():
            self.set(key, value)

    @classmethod
    def get_subclasses(cls):
        """Get subclasses, recursively
        @rtype generator
        """
        for subcls in cls.__subclasses__():
            yield subcls
            for subsubcls in subcls.get_subclasses():
                yield subsubcls

    def __getattr__(self, name):
        """Get the attribute, but load it if it's not available yet"""
        if name in self.wrapped_attrs:
            cls = self.wrapped_attrs[name]
            # The reason we do this here and not in _init is because lxml
            # is inconsistant about when elements are initialised.
            # So we make this a lazy property.
            def _set_attr(new_item):
                if new_item:
                    self.set(name, str(new_item))
                else:
                    self.attrib.pop(name, None) # pylint: disable=no-member

            # pylint: disable=no-member
            value = cls(self.attrib.get(name, None), callback=_set_attr)
            setattr(self, name, value)
            return value
        raise AttributeError("Can't find attribute {}.{}"
                             .format(type(self).__name__, name))

    def __setattr__(self, name, value):
        """Set the attribute, update the attrib if needed"""
        if name in self.wrapped_attrs:
            # Don't call self.set or self.get (infinate loop)
            if value:
                self.attrib[name] = str(value)
            else:
                self.attrib.pop(name, None) # pylint: disable=no-member
        else:
            super(BaseElement, self).__setattr__(name, value)

    def get(self, name, default=None):
        """Get element attribute named, with addNS support."""
        if name in self.wrapped_attrs:
            value = getattr(self, name, None)
            # We check the boolean nature of the value, because empty
            # transformations and style attributes are equiv to not-existing
            ret = str(value) if value else (default or None)
            return ret
        return super(BaseElement, self).get(addNS(name), default)

    def set(self, name, value):
        """Set element attribute named, with addNS support."""
        if name in self.wrapped_attrs:
            # Always keep the local wrapped class up to date.
            setattr(self, name, self.wrapped_attrs[name](value))
            value = str(getattr(self, name))
            if not value:
                return
        super(BaseElement, self).set(addNS(name), value)

    def add(self, *children):
        """
        Like append, but will do multiple children and well return
        children or only child
        """
        for child in children:
            self.append(child)
        return children if len(children) > 1 else children[0]

    def set_random_id(self, suffix=None, size=4):
        """Sets the id attribute if it's not already set"""
        root = self.getroottree().getroot()
        self.set('id', root.get_unique_id(suffix, size=size))

    @property
    def root(self):
        """Get the root document element from any element descendent"""
        if self.getparent() is not None:
            return self.getparent().root
        return self

    def decendants(self):
        """Walks the element tree and yields all elements, parent first"""
        yield self
        for child in self:
            if hasattr(child, 'decendants'):
                for decendant in child.decendants():
                    yield decendant

    def xpath(self, pattern, namespaces=NSS):  # pylint: disable=dangerous-default-value
        """Wrap xpath call and add svg namespaces"""
        return super(BaseElement, self).xpath(pattern, namespaces=namespaces)

    def findall(self, pattern, namespaces=NSS):  # pylint: disable=dangerous-default-value
        """Wrap findall call and add svg namespaces"""
        return super(BaseElement, self).findall(pattern, namespaces=namespaces)

    def __str__(self):
        # We would do more here, but lxml is VERY unpleseant when it comes to
        # namespaces, basically over printing details and providing no
        # supression mechanisms to turn off xml's over engineering.
        return str(self.tag).split('}')[-1]


class ShapeElement(BaseElement):
    """Elements which have a visible reprisentation on the canvas"""
    @property
    def path(self):
        """Gets the outline or path of the element, this can be a simple bounding box for most"""
        return Path(self.get_path())

    @path.setter
    def path(self, path):
        self.set_path(path)

    def get_path(self):
        """Generate a path for this object which can inform the bounding box"""
        raise NotImplementedError("Path should be provided by svg element {}."
                                  .format(type(self).__name__))

    def set_path(self, path):
        """Set the path for this object (if possible)"""
        raise AttributeError("Path can not be set on this type of element: {} <- {}."
                             .format(type(self).__name__, path))

    def composed_transform(self):
        """Calculate every transform down to the root document node"""
        parent = self.getparent()
        if parent is not None and isinstance(parent, ShapeElement):
            return self.transform * parent.composed_transform()
        return self.transform

    def composed_style(self):
        """Calculate the final styles applied to this element"""
        # FUTURE: We could compose styles from class/css too.
        parent = self.getparent()
        if parent is not None and isinstance(parent, ShapeElement):
            return parent.composed_style() + self.style
        return self.style

    def bounding_box(self):
        """Returns the bounding box for the element as a BoundingBox object (x1, x2, y1, y2)"""
        return self.path.bounding_box()

    def get_center_position(self):
        """Returns object's center in terms of document units"""
        x, y = self.bounding_box().center()
        return x or 0, y or 0

    @property
    def label(self):
        """Returns the inkscape label"""
        return self.get('inkscape:label', None)


class OtherElements(BaseElement):
    """A bunch of other svg elements"""
    tag_names = [
        'desc',
        'filter',
        'font',
        'font-face',
        'format',
        'rdf',
        'type',
        'work',
        'style',
    ]


class FlowRegion(ShapeElement):
    """SVG Flow Region (SVG 2.0)"""
    tag_name = 'flowRegion'

    def get_path(self):
        # XXX: These empty paths mean the bbox for text elements will be nothing.
        return Path()

class FlowRoot(ShapeElement):
    """SVG Flow Root (SVG 2.0)"""
    tag_name = 'flowRoot'

    def get_path(self):
        # XXX: These empty paths mean the bbox for text elements will be nothing.
        return Path()

class FlowPara(ShapeElement):
    """SVG Flow Paragraph (SVG 2.0)"""
    tag_name = 'flowPara'

    def get_path(self):
        # XXX: These empty paths mean the bbox for text elements will be nothing.
        return Path()

class FilterPrimitive(BaseElement):
    """A bunch of different filter primitives"""
    tag_names = [
        'feBlend', 'feColorMatrix', 'feComponentTransfer', 'feComposite',
        'feConvolveMatrix', 'feDiffuseLighting', 'feDisplacementMap', 'feFlood',
        'feGaussianBlur', 'feImage', 'feMerge', 'feMorphology', 'feOffset',
        'feSpecularLighting', 'feTile', 'feTurbulence'
    ]

class Group(ShapeElement):
    """Any group element (layer or regular group)"""
    tag_name = 'g'
    is_layer = lambda self: self.groupmode == 'layer'

    def get_path(self):
        return Path()

    def bounding_box(self):
        bbox = BoundingBox(None)
        for child in self:
            if isinstance(child, ShapeElement):
                bbox += child.bounding_box()
        return bbox

    @property
    def groupmode(self):
        """Return the type of group this is"""
        return self.get('inkscape:groupmode', 'group')

class Anchor(Group):
    """An anchor or link tag"""
    tag_name = 'a'

class PathElement(ShapeElement):
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

class Pattern(BaseElement):
    """Patern element which is used in the def to control repeating fills"""
    tag_name = 'pattern'
    WRAPPED_ATTRS = BaseElement.WRAPPED_ATTRS + (('patternTransform', Transform),)

class Points(ShapeElement):
    """Provide a useful extension for points elements"""
    tag_name = 'points'
    get_path = lambda self: 'M' + self.get('points')


class Rectangle(ShapeElement):
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


class Circle(ShapeElement):
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


class Use(ShapeElement):
    """A 'use' element that links to another in the document"""
    tag_name = 'use'

    get_path = lambda self: self.ref().get_path()

    def ref(self):
        """Returns the referred to element if available"""
        return self.root.getElementById(self.get('xlink:href').strip('#'))

class ClipPath(Group):
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

class Guide(BaseElement):
    """An inkscape guide"""
    tag_name = 'sodipodi:guide'

    def __init__(self, *args, **kwargs):
        super(Guide, self).__init__(**kwargs)
        if args:
            self.move_to(*args)

    def move_to(self, pos_x, pos_y, angle=None):
        """
        Move this guide to the given x,y position,

        Angle can either be a float or integer, which will change the orientation.
        Or a pair of numbers (tuple) which will be set as the orientation directly.
        """
        self.set('position', "{:g},{:g}".format(float(pos_x), float(pos_y)))
        if isinstance(angle, str):
            if ',' not in angle:
                angle = float(angle)

        if isinstance(angle, (float, int)):
            # Generate orientation from angle
            angle = (math.sin(math.radians(angle)), -math.cos(math.radians(angle)))

        if isinstance(angle, (tuple, list)) and len(angle) == 2:
            angle = "{:g},{:g}".format(*angle)

        self.set('orientation', angle)

class Metadata(BaseElement):
    """Inkscape Metadata element"""
    tag_name = 'metadata'

class ForeignObject(BaseElement):
    """SVG foreignObject element"""
    tag_name = 'foreignObject'

class TextElement(ShapeElement):
    """A Text element"""
    tag_name = 'text'

    def get_path(self):
        return Path()

class TextPath(ShapeElement):
    """A textPath element"""
    tag_name = 'textPath'

    def append_superscript(self, text):
        """Adds a superscript tspan element"""
        self.append(Tspan(text, style="font-size:65%;baseline-shift:super"))

    def get_path(self):
        return Path()

class Tspan(ShapeElement):
    """A tspan text element"""
    tag_name = 'tspan'

    def get_path(self):
        return Path()

class Marker(Group):
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
