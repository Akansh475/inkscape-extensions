# coding=utf-8
#
# Copyright (C) 2018 Martin Owens <doctormo@gmail.com>
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
functions for digesting paths into a simple list structure
"""

import re
import copy

from math import atan2, cos, pi, sin, sqrt, acos, tan
from operator import add, mul

from .transforms import Transform, BoundingBox, Scale
from .utils import X, Y, classproperty, strargs, pairwise

if False: # pylint: disable=using-constant-test
    from typing import Type, Dict # pylint: disable=unused-import


LEX_REX = re.compile(r'([MLHVCSQTAZmlhvcsqtaz])([^MLHVCSQTAZmlhvcsqtaz]*)')
NONE = lambda obj: obj is not None


class InvalidPath(ValueError):
    """Raised when given an invalid path string"""


class Segment(object):
    """
    A segment in a Path. Shouldn't be created sep' from the Path() object
    but if needed can be created using the syntax:

    Line(x, y)
    Line((x, y)) # Same as above
    Line([xa, ya, xb, yb, xc, yc]) # where array is modified leaving b and c
    Line(Move(x, y)) # Where Move segment is converted to Line segment
    """
    # Number of arguments that follow this path commands letter
    num = -1

    # The full name of the segment (i.e. Line, Arc, etc)
    name = classproperty(lambda cls: cls.__name__)

    # The single letter represtation of this command (i.e. L, A, etc)
    cmd = classproperty(lambda cls: cls.name[0])

    # The next command, this is for automatic chains where the next command
    # isn't given, just a bunch on numbers which we automatically parse.
    get_next = classmethod(lambda cls: getattr(cls, '_next', cls))

    # The other command is relative to absolute, absolute to relative
    # Conversion, giving the class back that would make sense.
    get_other = classmethod(lambda cls: cls.get_class(cls.cmd.swapcase()))

    # Returns True/False if the command is relative/absolute
    # based on the case of the command
    isrelative = lambda self: self.cmd.islower()
    isabsolute = lambda self: self.cmd.isupper()

    # The precision of the numbers when converting to string
    number_template = "{:.6g}"

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (list, tuple)):
                # Passed in variable is parsed numbers (array) or
                # set of coords from some other process (tupple)
                args = args[0]
            elif isinstance(args[0], Segment):
                # Passed in variable is some other segment which
                # should be converted to this type.
                args = self._from_segment(args[0])

        if self.num == -1:
            raise InvalidPath("Bad Segment type (None)")
        if isinstance(args, list) and len(args) < self.num:
            raise InvalidPath("Bad arguments {}({})".format(self.name, args))
        elif isinstance(args, tuple) and len(args) != self.num:
            raise InvalidPath("Bad arguments {}({})".format(self.name, args))

        self.args = tuple([float(x) for x in args[:self.num]])
        if isinstance(args, list):
            del args[:self.num]

    _cmds = {} # type: Dict[str, Segment]

    @classmethod
    def get_class(cls, cmd):
        """Get the class for this command name"""
        cmd = cmd.strip()
        pool = cls.__subclasses__()
        while len(cls._cmds) < len(pool):
            segtype = pool[len(cls._cmds)]
            pool.extend(segtype.__subclasses__())
            cls._cmds[segtype.cmd] = segtype
        if cmd in cls._cmds:
            return cls._cmds[cmd]
        raise KeyError("Unknown path command: {}".format(cmd))

    @classmethod
    def _argt(cls, sep):
        return sep.join([cls.number_template] * cls.num)

    def __str__(self):
        return "{} {}".format(self.cmd, self._argt(" ").format(*self.args)).strip()

    def __repr__(self):
        return "{{}}({})".format(self._argt(", ")).format(self.name, *self.args)

    def __eq__(self, other):
        if type(self) == type(other): # pylint: disable=unidiomatic-typecheck
            return self.args == other.args
        if isinstance(other, tuple):
            return self.args == other
        if not isinstance(other, Segment):
            raise ValueError("Can't compare types")
        try:
            if self.isrelative() == other.isrelative():
                return self.to_curve([0, 0]) == other.to_curve([0, 0])
        except ValueError as err:
            pass
        return False

    def __add__(self, other):
        if self.isabsolute():
            return self.translate(other)
        return self

    def __mul__(self, other):
        return self.scale(other)

    x = property(lambda self: self.args[-2])
    y = property(lambda self: self.args[-1])
    all_x = property(lambda self: self.args[::2])
    all_y = property(lambda self: self.args[1::2])

    @property
    def points(self):
        """Returns a list of points in this path command, x and y only"""
        return tuple(zip(self.all_x, self.all_y))

    def bounding_box(self, prev): # pylint: disable=unused-argument
        """Returns a rough bounding box, similar to roughBBox returns: (x1, x2, y1, y2)"""
        return BoundingBox(Scale(*self.all_x), Scale(*self.all_y))

    def translate(self, coords, opr=add):
        """Translate or scale this path command by the given coords X/Y"""
        lst = [opr(val, coords[i % 2]) for i, val in enumerate(self.args)]
        return type(self)(lst)

    def scale(self, coords):
        """Scale this path command by the given coords X/Y"""
        return self.translate(coords, opr=mul)

    def rotate(self, angle, center_x, center_y):
        """Rotate this path command around the given center, angle is given in degrees"""
        ans = []
        for (x, y) in self.points:  # pylint: disable=invalid-name
            offset_x = x - center_x
            offset_y = y - center_y
            theta = (atan2(offset_y, offset_x) + angle * pi / 180)
            rad = sqrt((offset_x ** 2) + (offset_y ** 2))
            ans.extend([rad * cos(theta) + center_x, rad * sin(theta) + center_y])
        return type(self)(ans) # pylint: disable=no-value-for-parameter

    def transform(self, transform, raw=False):
        """Apply a matrix transform to this path and return a new path"""
        transform = Transform(transform)
        points = list(self.points)
        for index, (x, y) in enumerate(points):
            points[index] = transform.apply_to_point([x, y])
        if raw:
            return points
        return type(self)([coord for point in points for coord in point])

    def get_pen(self, previous=(0, 0)):
        """Where will the pen be after this command"""
        if not self.isabsolute():
            self = self.translate(previous)
        if self.num:
            return self.points[-1]
        return previous

    def to_curve(self, previous):
        """Convert the segment into a curve segment"""
        raise NotImplementedError("To curve not supported for {}".format(self.name))

    def to_curves(self, previous):
        """Convert to segment, but returns an array of segments"""
        return [self.to_curve(previous)]

    @classmethod
    def _from_segment(cls, segment):
        """
        How is a segment (any segment) converted to this type? The default
        is for Line and Move, which takes only the next x,y coord pair.

        Others must be over-ridden to make sense of their inputs.
        """
        if segment.num == cls.num:
            return segment.args
        if cls.num == 2:
            return (segment.x, segment.y)
        raise NotImplementedError("Can not convert from {} to {}".format(segment.name, cls.name))

class Line(Segment):
    """Line segment"""
    num = 2

    def to_curve(self, previous):
        previous = Move(previous)
        return Curve(previous.x, previous.y, self.x, self.y, self.x, self.y)

class line(Line): # pylint: disable=invalid-name
    """Relative line segment"""

class Move(Segment):
    """Move pen segment without a line"""
    _next = Line
    num = 2

    def to_curve(self, previous):
        raise ValueError("Move segments can not be changed into curves.")

class move(Move): # pylint: disable=invalid-name
    """Relative move segment"""
    _next = line

class ZoneClose(Segment):
    """Close segment to finish a path"""
    _next = Move
    num = 0

class zoneClose(ZoneClose): # pylint: disable=invalid-name
    """Same as above (svg says no difference)"""

class Horz(Segment):
    """Horizontal Line segment"""
    num = 1
    x = property(lambda self: self.args[0])
    y = property(lambda self: None)
    points = property(lambda self: ((self.x, self.y),))

    def get_pen(self, previous=(0, 0)):
        """When getting the pen for Horz moves, we return the combined point"""
        pen = super(Horz, self).get_pen(previous)
        return tuple(pen[i] is None and previous[i] or pen[i] for i in (0, 1))

    def translate(self, coords, opr=add):
        """Translate this Horz path by the given coords X/Y"""
        return Horz(opr(self.args[0], coords[X]))

    def transform(self, transform, raw=False):
        raise ValueError("Hozontal lines can't be transformed directly.")

    def to_line(self, previous):
        """Return this path command as a line instead"""
        return Line(self.x, Move(previous).y)

    def to_curve(self, previous):
        """Convert a horzontal line into a curve"""
        previous = Move(previous)
        return self.to_line(previous).to_curve(previous)

class horz(Horz): # pylint: disable=invalid-name
    """Relative horz line segment"""

class Vert(Horz):
    """Vertical Line segment"""
    x = property(lambda self: None)
    y = property(lambda self: self.args[0])
    all_x = property(lambda self: [])
    all_y = property(lambda self: [self.y])

    def translate(self, coords, opr=add):
        """Translate this Horz path by the given coords X/Y"""
        return Vert(opr(self.args[0], coords[Y]))

    def to_line(self, previous):
        """Return this path command as a line instead"""
        return Line(Move(previous).x, self.y)

class vert(Vert): # pylint: disable=invalid-name
    """Relative vertical line segment"""

class Curve(Segment):
    """Absolute Curved Line segment"""
    num = 6

    x1 = property(lambda self: self.args[0])
    y1 = property(lambda self: self.args[1])
    x2 = property(lambda self: self.args[2])
    y2 = property(lambda self: self.args[3])

    def to_curve(self, previous):
        """No conversion needed, pass-through, returns self"""
        return self

class curve(Curve): # pylint: disable=invalid-name
    """Relative curved line segment"""

class Smooth(Segment):
    """Absolute Smoothed Curved Line segment"""
    num = 4

    x2 = property(lambda self: self.args[0])
    y2 = property(lambda self: self.args[1])

    def to_curve(self, previous):
        """
        Convert this Smooth curve to a regular curve by creating a mirror
        set of nodes based on the previous node. Previous should be a curve.
        """
        last = previous.to_curve(Line([0, 0]))
        x1 = (2 * last.x) - last.x2
        y1 = (2 * last.y) - last.y2
        return Curve(x1, y1, self.x2, self.y2, self.x, self.y)


class smooth(Smooth): # pylint: disable=invalid-name
    """Relative smoothed curved line segment"""

class Quadratic(Segment):
    """Absolute Quadratic Curved Line segment"""
    num = 4

    x1 = property(lambda self: self.args[0])
    y1 = property(lambda self: self.args[1])

    def to_curve(self, previous):
        """Attempt to convert a quadratic to a curve"""
        previous = Move(previous)
        x1 = 1. / 3 * previous.x + 2. / 3 * self.x1
        x2 = 2. / 3 * self.x1 + 1. / 3 * self.x
        y1 = 1. / 3 * previous.y + 2. / 3 * self.y1
        y2 = 2. / 3 * self.y1 + 1. / 3 * self.y
        return Curve(x1, y1, x2, y2, self.x, self.y)


class quadratic(Quadratic): # pylint: disable=invalid-name
    """Relative quadratic line segment"""

class TepidQuadratic(Segment):
    """Continued Quadratic Line segment"""
    num = 2

    def to_curve(self, previous):
        return self.to_quadratic(previous).to_curve(previous)

    def to_quadratic(self, previous):
        """
        Convert this continued quadratic into a full quadratic
        """
        last = previous.to_curve(Line([0, 0]))
        x1 = (last.x - last.x2) * 3. / 2 + last.x
        y1 = (last.y - last.y2) * 3. / 2 + last.y
        return Quadratic(x1, y1, self.x, self.y)


class tepidQuadratic(TepidQuadratic): # pylint: disable=invalid-name
    """Relative continued quadratic line segment"""

class Arc(Segment):
    """Special Arc segment"""
    num = 7
    points = property(lambda self: (self.args[-2:],))

    def bounding_box(self, prev):
        """Returns a bounding box for curved lines, similar to refinedBBox"""
        bbox = BoundingBox(None)
        for seg in self.to_curves(prev):
            bbox += seg.bounding_box(prev)
            prev = seg
        return bbox

    def to_curves(self, previous=(0, 0)):
        """Convert this arc into bezier curves"""
        if isinstance(previous, Segment):
            previous = previous.get_pen()
        cubic = arc_to_path(list(previous), list(self.args))
        for seg in CubicSuperPath([cubic]).to_segments():
            if isinstance(seg, Curve):
                yield seg

    def translate(self, coords, opr=add):
        """Translate or scale this path command by the given coords X/Y"""
        lst = self.args[:5] + (opr(self.args[5], coords[X]), opr(self.args[6], coords[Y]))
        return type(self)(list(lst))

    def transform(self, transform, raw=True):
        """Transform this arc along with the given transformation"""
        points = super(Arc, self).transform(transform, raw=True)[0]
        return Arc(self.args[:-2] + tuple(points))

    def scale(self, coords):
        """Scale the Arc by the given coords"""
        (x, y) = coords  # pylint: disable=invalid-name
        return Arc([
            self.args[0] * x,  # Radius
            self.args[1] * x,  # Radius
            (self.args[2], 0)[y < 0],  # X-axis rotation angle
            self.args[3],  # Unknown param '0'
            (self.args[4], 1 - self.args[4])[x * y < 0],  # sweep-flag
            self.args[5] * x,  # X coord
            self.args[6] * y,  # Y coord
        ])

class arc(Arc): # pylint: disable=invalid-name
    """Relative Arc line segment"""

class Path(list):
    """A list of segment commands which combine to draw a shape"""

    def __init__(self, path_d=None):
        super(Path, self).__init__()
        if isinstance(path_d, str):
            # Returns a generator returning Segment objects
            path_d = self.parse_string(path_d)
        elif isinstance(path_d, CubicSuperPath):
            path_d = path_d.to_path()

        for item in (path_d or ()):
            if isinstance(item, Segment):
                self.append(item)
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                if isinstance(item[1], (list, tuple)):
                    self.append(Segment.get_class(item[0])(*item[1]))
                else:
                    self.append(Line(*item))

    @classmethod
    def parse_string(cls, path_d):
        """Parse a path string and generate segment objects"""
        for cmd, numbers in LEX_REX.findall(path_d):
            args = list(strargs(numbers))
            cmd = Segment.get_class(cmd)
            while args or cmd.num == 0:
                seg = cmd(args)
                cmd = seg.get_next()
                yield seg

    def bounding_box(self):
        """Return the top,left and bottom,right coords"""
        return sum([seg.bounding_box(prev) \
            for prev, seg in pairwise(self.to_absolute(curves=True)) \
                if seg])

    def append(self, cmd):
        """Append a command to this path including any chained commands"""
        if isinstance(cmd, list):
            self.extend(cmd)
        elif isinstance(cmd, Segment):
            super(Path, self).append(cmd)

    def translate(self, x, y):  # pylint: disable=invalid-name
        """Move all coords in this path by the given amount"""
        for i, seg in enumerate(self):
            self[i] = seg + (x, y)

    def scale(self, x, y):  # pylint: disable=invalid-name
        """Scale all coords in this path by the given amounts"""
        for i, seg in enumerate(self):
            self[i] = seg * (x, y)

    def rotate(self, angle, center_x=None, center_y=None):
        """Rotate the path around the given point"""
        if center_x is None or center_y is None:
            # Default center is center of bbox
            center = self.bounding_box().center()
            center_x = center_x or center[0]
            center_y = center_y or center[1]
        pen = (0.0, 0.0)
        for i, seg in enumerate(self):
            if seg.num == 1:
                # Vertical and Horizontal lines can not be rotated
                seg = seg.to_line(pen)
            if seg.num:
                pen = self[i].get_pen(pen)
                self[i] = seg.rotate(angle, center_x, center_y)

    def transform(self, transform):
        """Convert to new path"""
        for i, seg in enumerate(self):
            if isinstance(seg, (Horz, Vert)):
                previous = self[i-1] if i else (0, 0)
                seg = seg.to_line(previous)
            self[i] = seg.transform(transform)
        return self

    def reverse(self):
        """Returns a reversed path"""
        pass

    def to_absolute(self, factor=1, curves=False):
        """Convert this path to use only absolute coordinates"""
        pen = (0.0, 0.0)
        new_path = Path()
        for seg in self:
            if curves and isinstance(seg, Arc):
                # Force arcs to curves here
                segs = list(seg.to_curves(pen))
            elif seg.isrelative() != (factor == -1):

                segs = [seg.get_other()(
                    list(seg.translate((pen[0] * factor, pen[1] * factor)).args)
                )]
            else:
                segs = [seg]

            new_path.extend(segs)
            pen = new_path[-1].get_pen(pen)
        return new_path

    def to_relative(self):
        """Convert this path to use only relative coordinates"""
        return self.to_absolute(factor=-1)

    def __str__(self):
        return " ".join([str(seg) for seg in self])

    def __add__(self, other):
        acopy = copy.copy(self)
        if isinstance(other, tuple):
            acopy.translate(other[X], other[Y])
        if isinstance(other, str):
            other = Path(other)
        if isinstance(other, list):
            acopy.extend(other)
        return acopy

    def __mul__(self, other):
        acopy = copy.copy(self)
        acopy.scale(other[X], other[Y])
        return acopy

    def __sub__(self, other):
        return self.__add__((other[X] * -1, other[Y] * -1))

    def to_arrays(self):
        """Duplicates the original output of parsePath, returning arrays of segment data"""
        return [[seg.cmd, list(seg.args)] for seg in self.to_absolute()]

    def to_superpath(self):
        """Convert this path into a cubic super path"""
        return CubicSuperPath(self)

    def copy(self):
        """Make a copy"""
        return copy.copy(self)


class CubicSuperPath(list):
    """
    A conversion of a path into a predictable list of cubic curves which
    can be operated on as a list of simplified instructions.

    When converting back into a path, all lines, arcs etc will be coverted
    to curve instructions.

    Structure is held as [SubPath[(point_a, bezier, point_b), ...]], ...]
    """
    def __init__(self, items):
        super(CubicSuperPath, self).__init__()
        self._closed = True
        self._prev = Move([0, 0])

        if isinstance(items, str):
            items = Path(items)

        if isinstance(items, Path):
            items = items.to_absolute()

        for item in items:
            self.append(item)

    def __str__(self):
        return str(self.to_path())

    def append(self, item):
        """Accept multiple different formats for the data"""
        if isinstance(item, list) and len(item) == 2 and isinstance(item[0], str):
            item = Segment.get_class(item[0])(*item[1])
        if isinstance(item, Segment):
            if isinstance(item, Move):
                item, self._prev = [list(item.args), list(item.args), list(item.args)], item
            elif isinstance(item, ZoneClose) and self and self[-1]:
                # This duplicates the first segment to 'close' the path, it's appended directly
                # because we don't want to last coord to change for the final segment.
                self[-1].append([self[-1][0][0][:], self[-1][0][1][:], self[-1][0][2][:]])
                # Then adds a new subpath for the next shape (if any)
                self.closed = True
                self._prev = Move([0, 0])
                return
            elif isinstance(item, Arc):
                # Arcs are made up of three curves (approximated)
                for arc_curve in item.to_curves(self._prev):
                    self.append(arc_curve)
                return
            else:
                if isinstance(item, (Horz, Vert)):
                    item = item.to_line(self._prev)
                item, self._prev = item.to_curve(self._prev), item

        if isinstance(item, Curve):
            # Curves are cut into three tuples for the super path.
            item = [list(item.args[:2]), list(item.args[2:4]), list(item.args[4:6])]

        if not isinstance(item, list):
            raise ValueError("Unknown super curve item type: {}".format(item))

        if len(item) != 3 or not all([len(bit) == 2 for bit in item]):
            # The item is already a subpath (usually from some other process)
            if len(item[0]) == 3 and all([len(bit) == 2 for bit in item[0]]):
                return super(CubicSuperPath, self).append(item)
            raise ValueError("Unknown super curve list format: {}".format(item))

        if self._closed:
            # Closed means that the previous segment is closed so we need a new one
            # We always append to the last open segment. CSP starts out closed.
            self._closed = False
            super(CubicSuperPath, self).append([])

        if self[-1]:
            # The last tuple is replaced, it's the coords of where the next segment will land.
            self[-1][-1][-1] = item[0][:]
        # The last coord is duplicated, but is expected to be replaced
        self[-1].append(item[1:] + copy.deepcopy(item)[-1:])

    def to_path(self):
        """Convert the super path back to an svg path"""
        return Path(list(self.to_segments()))

    def to_segments(self):
        """Generate a set of segments for this cubic super path"""
        for subpath in self:
            previous = []
            for segment in subpath:
                if not previous:
                    yield Move(segment[1][:])
                else:
                    yield Curve(previous[2][:] + segment[0][:] + segment[1][:])
                previous = segment

    def transform(self, transform):
        """Apply a transformation matrix to this super path"""
        return self.to_path().transform(transform).to_superpath()

def arc_to_path(point, params):
    """Approximates an arc with cubic bezier segments.

    Arguments:
    point:  Starting point (absolute coords)
    params: Arcs parameters as per
              https://www.w3.org/TR/SVG/paths.html#PathDataEllipticalArcCommands

    Returns a list of triplets of points : [control_point_before, node, control_point_after]
    (first and last returned triplets are [p1, p1, *] and [*, p2, p2])
    """
    A = point[:]
    rx, ry, teta, longflag, sweepflag, x2, y2 = params[:]
    teta = teta * pi / 180.0
    B = [x2, y2]
    # Degenerate ellipse
    if rx == 0 or ry == 0 or A == B:
        return [[A[:], A[:], A[:]], [B[:], B[:], B[:]]]

    # turn coordinates so that the ellipse morph into a *unit circle* (not 0-centered)
    mat = matprod((rotmat(teta), [[1 / rx, 0], [0, 1 / ry]], rotmat(-teta)))
    applymat(mat, A)
    applymat(mat, B)

    k = [-(B[1] - A[1]), B[0] - A[0]]
    d = k[0] * k[0] + k[1] * k[1]
    k[0] /= sqrt(d)
    k[1] /= sqrt(d)
    d = sqrt(max(0, 1 - d / 4))
    # k is the unit normal to AB vector, pointing to center O
    # d is distance from center to AB segment (distance from O to the midpoint of AB)
    # for the last line, remember this is a unit circle, and kd vector is ortogonal to AB (Pythagorean thm)

    if longflag == sweepflag: #top-right ellipse in SVG example https://www.w3.org/TR/SVG/images/paths/arcs02.svg
        d *= -1

    O = [(B[0] + A[0]) / 2 + d * k[0], (B[1] + A[1]) / 2 + d * k[1]]
    OA = [A[0] - O[0], A[1] - O[1]]
    OB = [B[0] - O[0], B[1] - O[1]]
    start = acos(OA[0] / norm(OA))
    if OA[1] < 0:
        start *= -1
    end = acos(OB[0] / norm(OB))
    if OB[1] < 0:
        end *= -1
    # start and end are the angles from center of the circle to A and to B respectively

    if sweepflag and start > end:
        end += 2 * pi
    if (not sweepflag) and start < end:
        end -= 2 * pi

    NbSectors = int(abs(start - end) * 2 / pi) + 1
    dTeta = (end - start) / NbSectors
    v = 4 * tan(dTeta / 4) / 3
    # I would use v = tan(dTeta/2)*4*(sqrt(2)-1)/3 ?
    p = []
    for i in range(0, NbSectors + 1, 1):
        angle = start + i * dTeta
        v1 = [O[0] + cos(angle) - (-v) * sin(angle), O[1] + sin(angle) + (-v) * cos(angle)]
        pt = [O[0] + cos(angle), O[1] + sin(angle)]
        v2 = [O[0] + cos(angle) - v * sin(angle), O[1] + sin(angle) + v * cos(angle)]
        p.append([v1, pt, v2])
    p[0][0] = p[0][1][:]
    p[-1][2] = p[-1][1][:]

    # go back to the original coordinate system
    mat = matprod((rotmat(teta), [[rx, 0], [0, ry]], rotmat(-teta)))
    for pts in p:
        applymat(mat, pts[0])
        applymat(mat, pts[1])
        applymat(mat, pts[2])
    return p

def matprod(mlist):
    """Get the product of the mat"""
    prod = mlist[0]
    for mat in mlist[1:]:
        a00 = prod[0][0] * mat[0][0] + prod[0][1] * mat[1][0]
        a01 = prod[0][0] * mat[0][1] + prod[0][1] * mat[1][1]
        a10 = prod[1][0] * mat[0][0] + prod[1][1] * mat[1][0]
        a11 = prod[1][0] * mat[0][1] + prod[1][1] * mat[1][1]
        prod = [[a00, a01], [a10, a11]]
    return prod

def rotmat(teta):
    """Rotate the mat"""
    return [[cos(teta), -sin(teta)], [sin(teta), cos(teta)]]

def applymat(mat, point):
    """Apply the given mat"""
    x = mat[0][0] * point[0] + mat[0][1] * point[1]
    y = mat[1][0] * point[0] + mat[1][1] * point[1]
    point[0] = x
    point[1] = y

def norm(point):
    """Normalise"""
    return sqrt(point[0] * point[0] + point[1] * point[1])
