# coding=utf-8
#
# Copyright (C) 2006 Jean-Francois Barraud, barraud@math.univ-lille1.fr
# Copyright (C) 2010 Alvin Penner, penner@vaxxine.com
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
# barraud@math.univ-lille1.fr
#
# This code defines several functions to make handling of transform
# attribute easier.
#
"""
Provide transformation parsing to extensions
"""

import re
from decimal import Decimal
from math import cos, radians, sin, sqrt, tan, fabs, atan2, pi

from .utils import X, Y, strargs

class Transform(object):
    """A transformation object which will always reduce to a matrix and can
    then be used in combination with other transformations for reducing
    finding a point and printing svg ready output.

    Use with svg transform attribute input:

      tr = Transform("scale(45, 32)")

    Use with triplet matrix input (internal repr):

      tr = Transform(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)))

    Use with sixtlet matrix input (i.e. svg matrix(...)):

      tr = Transform((1.0, 0.0, 0.0, 1.0, 0.0, 0.0))

    Once you have a transformation you can operate tr * tr to compose,
    any of the above inputs are also valid operators for composing.
    """
    TRM = re.compile(r'(translate|scale|rotate|skewX|skewY|matrix)\s*\(([^)]*)\)\s*,?')

    def __init__(self, matrix=None, callback=None, **extra):
        self.callback = None
        self.matrix = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        if matrix is not None:
            # We parse a given string as an svg transformation instruction
            if isinstance(matrix, str):
                for func, values in self.TRM.findall(matrix.strip()):
                    getattr(self, 'add_' + func.lower())(*strargs(values))
            elif isinstance(matrix, Transform):
                self.matrix = matrix.matrix
            elif not isinstance(matrix, (tuple, list)):
                raise ValueError("Given transformation isn't a valid input")
            elif len(matrix) == 2:
                self.matrix = tuple(matrix[0]), tuple(matrix[1])
            elif len(matrix) == 6:
                self.matrix = tuple(matrix[::2]), tuple(matrix[1::2])
            else:
                raise ValueError("Matrix '{}' is not a valid transformation matrix".format(matrix))
        elif extra:
            for key in list(extra):
                if hasattr(self, 'add_' + key):
                    value = extra.pop(key)
                    func = getattr(self, 'add_' + key)
                    if isinstance(value, tuple):
                        func(*value)
                    else:
                        func(value)
        # Set callback last, so it doesn't kick off just setting up the internal value
        self.callback = callback

    # These provide quick access to the svg matrix:
    #
    # [ a, c, e ]
    # [ b, d, f ]
    #
    a = property(lambda self: self.matrix[0][0])  # pylint: disable=invalid-name
    b = property(lambda self: self.matrix[1][0])  # pylint: disable=invalid-name
    c = property(lambda self: self.matrix[0][1])  # pylint: disable=invalid-name
    d = property(lambda self: self.matrix[1][1])  # pylint: disable=invalid-name
    e = property(lambda self: self.matrix[0][2])  # pylint: disable=invalid-name
    f = property(lambda self: self.matrix[1][2])  # pylint: disable=invalid-name

    def __bool__(self):
        return not self.__eq__(Transform())
    __nonzero__ = __bool__

    def add_matrix(self, *args):
        """Add matrix in order they appear in the svg sixtlet"""
        self.__imul__(Transform(args))

    def add_translate(self, tr_x, tr_y=0.0):
        """Add translation to this transformation"""
        self.__imul__(((1.0, 0.0, tr_x), (0.0, 1.0, tr_y)))

    def add_scale(self, sc_x, sc_y=None):
        """Add scale to this transformation"""
        sc_y = sc_x if sc_y is None else sc_y
        self.__imul__(((sc_x, 0.0, 0.0), (0.0, sc_y, 0.0)))

    def add_rotate(self, deg, center_x=0.0, center_y=0.0):
        """Add rotation to this transformation"""
        _cos, _sin = cos(radians(deg)), sin(radians(deg))
        self.__imul__(((_cos, -_sin, center_x), (_sin, _cos, center_y)))
        self.__imul__(((1.0, 0.0, -center_x), (0.0, 1.0, -center_y)))

    def add_skewx(self, deg):
        """Add skew x to this transformation"""
        self.__imul__(((1.0, tan(radians(deg)), 0.0), (0.0, 1.0, 0.0)))

    def add_skewy(self, deg):
        """Add skew y to this transformation"""
        self.__imul__(((1.0, 0.0, 0.0), (tan(radians(deg)), 1.0, 0.0)))

    def to_sixlet(self):
        """Returns the transform as a sixtlet matrix (used in svg)"""
        return (val for lst in zip(*self.matrix) for val in lst)

    def __str__(self):
        """Format the given matrix into a string repr for svg"""
        sixlet = tuple(self.to_sixlet())
        if sixlet[:4] == (1, 0, 0, 1):
            if sixlet[4:] == (0, 0):
                return ""
            return "translate({:.6g}, {:.6g})".format(*sixlet[4:])
        elif sixlet[4:] == (0, 0) and sixlet[1:3] == (0, 0):
            return "scale({:.6g}, {:.6g})".format(sixlet[0], sixlet[3])
        return "matrix({})".format(" ".join(format(var, '.6g') for var in sixlet))

    def __repr__(self):
        """String Representation of this object"""
        return "{}((({}), ({})))".format(
            type(self).__name__,
            ', '.join(format(var, '.6g') for var in self.matrix[0]),
            ', '.join(format(var, '.6g') for var in self.matrix[1]))

    def __eq__(self, matrix):
        """Test if this transformation is equal to the given matrix"""
        return self.matrix == Transform(matrix).matrix

    def __mul__(self, matrix):
        """Combine this transform's internal matrix with the given matrix"""
        # Conform the input to a known quantity (and convert if needed)
        other = Transform(matrix)
        # Return a transformation as the combined result
        return Transform((
            self.a * other.a + self.c * other.b,
            self.b * other.a + self.d * other.b,
            self.a * other.c + self.c * other.d,
            self.b * other.c + self.d * other.d,
            self.a * other.e + self.c * other.f + self.e,
            self.b * other.e + self.d * other.f + self.f))

    def __imul__(self, matrix):
        """In place multiplication of transformat matricies"""
        self.matrix = (self * matrix).matrix
        if self.callback is not None:
            self.callback(self)
        return self

    def __neg__(self):
        """Returns an inverted transformation"""
        det = (self.a * self.d) - (self.c * self.b)
        # invert the rotation/scaling part
        new_a = self.d / det
        new_d = self.a / det
        new_c = -self.c / det
        new_b = -self.b / det
        # invert the translational part
        new_e = -(new_a * self.e + new_c * self.f)
        new_f = -(new_b * self.e + new_d * self.f)
        return Transform((new_a, new_b, new_c, new_d, new_e, new_f))

    def apply_to_point(self, point):
        """Transform a tuple (X, Y)"""
        if isinstance(point, str):
            raise ValueError("Will not transform string '{}'".format(point))
        return (self.a * point[X] + self.c * point[Y] + self.e,
                self.b * point[X] + self.d * point[Y] + self.f)

class TranslateTransform(Transform):
    """A quick and easy to use Translate definition"""
    def __init__(self, pos_x, pos_y=0.0):
        super(TranslateTransform, self).__init__()
        self.add_translate(pos_x, pos_y)

class ScaleTransform(Transform):
    """A quick and easy to use Scale definition"""
    def __init__(self, scale_x, scale_y=None):
        super(ScaleTransform, self).__init__()
        self.add_scale(scale_x, scale_y)

class RotateTransform(Transform):
    """A quick and easy to use Rotate definiiton"""
    def __init__(self, deg, center_x=0.0, center_y=0.0):
        super(RotateTransform, self).__init__()
        self.add_rotate(deg, center_x, center_y)


class Scale(object):  # pylint: disable=too-few-public-methods
    """A pair of numbers that reprisent the minimum and maximum values."""

    def __init__(self, value=None, *others):
        if isinstance(value, Scale):
            self.maximum = value.maximum
            self.minimum = value.minimum
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            (self.minimum, self.maximum) = value
        elif isinstance(value, (int, float, Decimal)):
            self.minimum = value
            self.maximum = value
        elif value is None:
            self.minimum = None
            self.maximum = None
        else:
            raise ValueError("Not a number for scaling: {} ({})" \
                             .format(str(value), type(value).__name__))

        for item in others:
            self += item

    def __bool__(self):
        return self.minimum is not None and self.maximum is not None
    __nonzero__ = __bool__

    def __add__(self, other):
        return Scale(other) + self

    def __iadd__(self, other):
        other = Scale(other)
        if self.minimum is None:
            self.minimum = other.minimum
        elif other.minimum is not None:
            self.minimum = min((self.minimum, other.minimum))
        if self.maximum is None:
            self.maximum = other.maximum
        elif other.maximum is not None:
            self.maximum = max((self.maximum, other.maximum))
        return self

    def __radd__(self, other):
        if other != 0:  # ignore sum() initial value
            return self + other
        return self

    def __mul__(self, other):
        new = Scale(self)
        if other is not None:
            new *= other
        return new

    def __imul__(self, other):
        self.minimum *= other
        self.maximum *= other
        return self

    def __iter__(self):
        yield self.minimum
        yield self.maximum

    def __eq__(self, other):
        return tuple(self) == tuple(Scale(other))

    def __repr__(self):
        return "scale:" + str(tuple(self))

    @property
    def center(self):
        """Pick the middle of the line"""
        if self.minimum is None or self.maximum is None:
            return None
        return self.minimum + ((self.maximum - self.minimum) / 2)

    @property
    def size(self):
        """Return the size difference minimum and manximum"""
        if self.minimum is None or self.maximum is None:
            return None
        return self.maximum - self.minimum


class BoundingBox(object):  # pylint: disable=too-few-public-methods
    """
    Some functions to compute a rough bbox of a given list of objects.

    BoundingBox() - Empty bounding box, bool == False
    BoundingBox(x)
    BoundingBox(x, y)
    BoundingBox((x1, x2, y1, y2))
    BoundingBox((x1, x2), (y1, y2))
    BoundingBox(((x1, y1), (x2, y2)))
    """
    width = property(lambda self: self.x.size)
    height = property(lambda self: self.y.size)
    top = property(lambda self: self.y.minimum)
    left = property(lambda self: self.x.minimum)
    bottom = property(lambda self: self.y.maximum)
    right = property(lambda self: self.x.maximum)

    def __init__(self, x=None, y=None):
        if y is None:
            if isinstance(x, BoundingBox):
                x, y = x.x, x.y
            elif isinstance(x, (list, tuple)):
                if len(x) == 2:
                    if isinstance(x[0], (list, tuple)):
                        y = x[0][1], x[1][1]
                        x = x[0][0], x[1][0]
                    else:
                        x, y = x
                elif len(x) == 4:
                    x, y = x[:2], x[2:]
        self.x = Scale(x)
        self.y = Scale(y)

    def __bool__(self):
        return bool(self.x) and bool(self.y)
    __nonzero__ = __bool__

    def __add__(self, other):
        new = BoundingBox(self.x, self.y)
        if other is not None:
            new += other
        return new

    def __iadd__(self, other):
        other = BoundingBox(other)
        self.x += other.x
        self.y += other.y
        return self

    def __radd__(self, other):
        if other != 0:
            return self + other
        return self

    def __mul__(self, other):
        new = BoundingBox(self.x, self.y)
        if other is not None:
            new *= other
        return new

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __eq__(self, other):
        if isinstance(other, (tuple, BoundingBox)):
            return tuple(self) == tuple(other)
        return False

    def __iter__(self):
        yield self.x.minimum
        yield self.x.maximum
        yield self.y.minimum
        yield self.y.maximum

    @property
    def minimum(self):
        """Return the minimum x,y coords"""
        return (self.x.minimum, self.y.minimum)

    @property
    def maximum(self):
        """Return the maximum x,y coords"""
        return (self.x.maximum, self.y.maximum)

    def __getitem__(self, index):
        return list(self)[index]

    def __repr__(self):
        return "BoundingBox({})".format(str(tuple(self)))

    def center(self):
        """Returns the middle of the bounding box"""
        return self.x.center, self.y.center

class Segment(BoundingBox):
    """
    A segment and a bounding box are functionally the same, except that
    the coords mean something slightly different.

    Segment(x1, x2, y1, y2)
    Segment(((x1, y1), (x2, y2)))
    """
    @property
    def length(self):
        """Get the length from the top left to the bottom right of the line"""
        return sqrt((self.width ** 2) + (self.height ** 2))

    @property
    def angle(self):
        """Get the angle of the line created by this segment"""
        return pi * (atan2(self.height, self.width)) / 180

    def distance_to_point(self, x, y):
        """Get the distance to the given point (x, y)"""
        segment2 = Segment((self.minimum, (x, y)))
        dot2 = segment2.dot(self)
        if dot2 <= 0:
            return Segment(((x, y), self.minimum)).length
        if self.dot(self) <= dot2:
            return Segment(((x, y), self.maximum)).length
        return self.perp_distance(x, y)

    def perp_distance(self, x, y):
        """Perpendicular distance to the given point"""
        if self.length == 0:
            return None
        return fabs((self.width * (self.top - y)) - ((self.left - x) * self.height)) / self.length

    def dot(self, other):
        """Get the dot of the segment (what is dot, we don't know)"""
        return self.width * other.width + self.height * other.height

    def point_at_ratio(self, ratio):
        """Get the point at the given ratio along the line"""
        if self.length == 0:
            return (None, None)
        return (self.left + (ratio * self.width),
                self.top + (ratio * self.height))

    def intersect(self, other):
        """Get the intersection betwene two segments"""
        other = Segment(other)
        denom = (other.height * self.width) - (other.width * self.height)
        num = (other.width * (self.top - other.top)) - (other.height * (self.left - other.left))
        #num2 = (self.width * (self.top - other.top)) - (self.height * (self.left - other.left))

        if denom != 0:
            return (
                self.left + ((num / denom) * (other.right - self.left)),
                self.top + ((num / denom) * (other.top - self.top))
            )
        return (None, None)

    def __repr__(self):
        return "Segment(({0.minimum}, {0.maximum}))".format(self)


def cubic_extrema(py0, py1, py2, py3):
    """Returns the extreme value, given a set of bezier coords"""
    cmin, cmax = min(py0, py3), max(py0, py3)
    pd1 = py1 - py0
    pd2 = py2 - py1
    pd3 = py3 - py2

    def _is_bigger(point):
        if (point > 0) and (point < 1):
            pyx = py0 * (1 - point) * (1 - point) * (1 - point) + \
                  3 * py1 * point * (1 - point) * (1 - point) + \
                  3 * py2 * point * point * (1 - point) + \
                  py3 * point * point * point
            return min(cmin, pyx), max(cmax, pyx)
        return cmin, cmax

    if pd1 - 2 * pd2 + pd3:
        if pd2 * pd2 > pd1 * pd3:
            pds = sqrt(pd2 * pd2 - pd1 * pd3)
            cmin, cmax = _is_bigger((pd1 - pd2 + pds) / (pd1 - 2 * pd2 + pd3))
            cmin, cmax = _is_bigger((pd1 - pd2 - pds) / (pd1 - 2 * pd2 + pd3))

    elif pd2 - pd1:
        cmin, cmax = _is_bigger(-pd1 / (2 * (pd2 - pd1)))

    return cmin, cmax

def quadratic_extrema(py0, py1, py2):
    def _is_bigger(point):
        if (point > 0) and (point < 1):
            pyx = py0 * (1 - point) * (1 - point) + \
                  2 * py1 * point * (1 - point) + \
                  py2 * point * point
            return min(cmin, pyx), max(cmax, pyx)
        return cmin, cmax
    cmin, cmax = min(py0, py2), max(py0, py2)
    if py0+py2-2*py1:
       cmin, cmax = _is_bigger((py0-py1)/(py0+py2-2*py1))
    return cmin, cmax

