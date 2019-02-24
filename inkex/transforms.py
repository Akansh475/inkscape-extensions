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
from math import cos, sin, tan, radians, sqrt
from decimal import Decimal

from .utils import strargs, X, Y


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

    def __init__(self, matrix=None):
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

    # These provide quick access to the svg matrix:
    #
    # [ a, c, e ]
    # [ b, d, f ]
    #
    a = property(lambda self: self.matrix[0][0]) # pylint: disable=invalid-name
    b = property(lambda self: self.matrix[1][0]) # pylint: disable=invalid-name
    c = property(lambda self: self.matrix[0][1]) # pylint: disable=invalid-name
    d = property(lambda self: self.matrix[1][1]) # pylint: disable=invalid-name
    e = property(lambda self: self.matrix[0][2]) # pylint: disable=invalid-name
    f = property(lambda self: self.matrix[1][2]) # pylint: disable=invalid-name

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
        self.__imul__((((1.0, 0.0, -center_x), (0.0, 1.0, -center_y))))

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
        return "matrix({})".format(" ".join(format(var, '.6g') for var in self.to_sixlet()))

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


class Scale(object): # pylint: disable=too-few-public-methods
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
            raise ValueError("Not a number for scaling: {} ({})"\
                .format(str(value), type(value).__name__))

        for item in others:
            self += item

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
        if other != 0: # ignore sum() initial value
            return self + other
        return self

    def __iter__(self):
        yield self.minimum
        yield self.maximum

    def __eq__(self, other):
        return tuple(self) == tuple(Scale(other))

    def __repr__(self):
        return "scale:" + str(tuple(self))

    def center(self):
        """Pick the middle of the line"""
        if self.minimum is None or self.maximum is None:
            return None
        return self.minimum + ((self.maximum - self.minimum) / 2)


class BoundingBox(object): # pylint: disable=too-few-public-methods
    """Some functions to compute a rough bbox of a given list of objects."""
    def __init__(self, x, y=None):
        if y is None:
            if isinstance(x, BoundingBox):
                x, y = x.x, x.y
            elif isinstance(x, (list, tuple)):
                if len(x) == 2:
                    x, y = x
                elif len(x) == 4:
                    x, y = x[:2], x[2:]
        self.x = Scale(x)
        self.y = Scale(y)

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

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __iter__(self):
        yield self.x.minimum
        yield self.x.maximum
        yield self.y.minimum
        yield self.y.maximum

    def __getitem__(self, index):
        return list(self)[index]

    def __repr__(self):
        return "bbox:" + str(tuple(self))

    def center(self):
        """Returns the middle of the bounding box"""
        return self.x.center(), self.y.center()

def cubicExtrema(py0, py1, py2, py3):
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
        if (pd2 * pd2 > pd1 * pd3):
            pds = sqrt(pd2 * pd2 - pd1 * pd3)
            cmin, cmax = _is_bigger((pd1 - pd2 + pds) / (pd1 - 2 * pd2 + pd3))
            cmin, cmax = _is_bigger((pd1 - pd2 - pds) / (pd1 - 2 * pd2 + pd3))

    elif (pd3 - pd1):
        cmin, cmax = _is_bigger(-pd1 / (pd3 - pd1))

    return cmin, cmax

def pairwise(iterable):
    "Iterate over a list with overlapping pairs (see itertools recipes)"
    from itertools import tee
    first, then = tee(iterable)
    next(then, None)
    return zip(first, then)

def path_loop(path):
     for pathcomp in path:
        for ctl in pathcomp:
            yield ctl

def roughBBox(path):
    """Returns a very basic bbox based on path points (no curve interpolation)"""
    x, y = [], []
    for ctl in path_loop(path):
        for pt in ctl:
            x.append(pt[X])
            y.append(pt[Y])
    return min(x), max(x), min(y), max(y)

def computeBBox(elements, mat=((1,0,0),(0,1,0))):
    from simpletransform import parseTransform
    bbox=None
    for node in elements:
        m = parseTransform(node.get('transform'))
        m = composeTransform(mat,m)
        #TODO: text not supported!
 
        if d is not None:
            p = inkex.parseCubicPath(d)
            applyTransformToPath(m, p)
            bbox=boxunion(refinedBBox(p), bbox)

        elif node.tag == inkex.addNS('use','svg') or node.tag=='use':
            refid=node.get(inkex.addNS('href','xlink'))
            path = '//*[@id="%s"]' % refid[1:]
            refnode = node.xpath(path)
            bbox=boxunion(computeBBox(refnode,m),bbox)

        bbox = boxunion(computeBBox(node,m), bbox)
    return bbox



# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
