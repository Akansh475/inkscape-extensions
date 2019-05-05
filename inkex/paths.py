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

from math import atan2, cos, pi, sin, sqrt
from operator import add, mul

from .transforms import Transform, BoundingBox, Scale
from .utils import X, Y, classproperty, strargs, pairwise
from .cubic_paths import unCubicSuperPath, ArcToPath

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
        print("Trying to compare {} == {} with {} == {}".format(
            self, other, self.to_curve([0, 0]), other.to_curve([0, 0]),
        ))
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
        x1 = (2 * last.x) - last.x1
        y1 = (2 * last.y) - last.y1
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
        x1 = (last.x - last.x1) * 3. / 2 + last.x
        y1 = (last.y - last.y1) * 3. / 2 + last.y
        return Quadratic(x1, y1, self.x, self.y)


class tepidQuadratic(Segment): # pylint: disable=invalid-name
    """Relative continued quadratic line segment"""

class Arc(Segment):
    """Special Arc segment"""
    num = 7
    points = property(lambda self: (self.args[-2:],))

    def bounding_box(self, prev):
        """Returns a bounding box for curved lines, similar to refinedBBox"""
        bbox = BoundingBox(None)
        for seg in self.to_curves(prev.get_pen()):
            bbox += seg.bounding_box(prev)
            prev = seg
        return bbox

    def to_curves(self, previous=(0, 0)):
        """Convert this arc into bezier curves"""
        cubic = ArcToPath(list(previous), list(self.args))
        for seg in unCubicSuperPath([cubic]):
            yield Segment.get_class(seg[0])(list(seg[1]))

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

        if isinstance(items, str):
            items = Path(items)

        for item in items:
            self.append(item)

        self._move = None

    def __str__(self):
        return str(self.to_path())

    def append(self, item):
        """Accept multiple different formats for the data"""
        if isinstance(item, Segment):
            if isinstance(item, Move):
                self._move = item
            else:
                item = item.to_absolute().to_curve()

        # TODO: Check format of item here
        super(CubicSuperPath, self).append(item)

    def to_path(self):
        """Convert the super path back to an svg path"""
        return Path(list(self._to_segments()))

    def _to_segments(self):
        for subpath in self:
            previous = []
            for segment in subpath:
                if not previous:
                    yield Move(segment[1][:])
                else:
                    yield Curve(previous[2][:] + segment[0][:] + segment[1][:])
                previous = segment
