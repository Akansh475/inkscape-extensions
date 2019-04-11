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

from .transforms import Transform, BoundingBox, Scale, cubic_extrema
from .utils import X, Y, classproperty, strargs, pairwise
from .cubic_paths import CubicSuperPath, unCubicSuperPath, ArcToPath

LEX_REX = re.compile(r'([MLHVCSQTAZmlhvcsqtaz])([^MLHVCSQTAZmlhvcsqtaz]*)')
NONE = lambda obj: obj is not None


class InvalidPath(ValueError):
    """Raised when given an invalid path string"""


class PathCommand(tuple):
    """A list of arguments that make up a segment, may return a list of
    command objects if the command string parsed was chained."""
    # Number of arguments that follow this path commands letter
    num = -1

    # The full name of the segment (i.e. Line, Arc, etc)
    name = classproperty(lambda cls: cls.__name__)

    # The single letter represtation of this command (i.e. L, A, etc)
    # This is always upper case and wouldn't be confused with self.cmd
    this_cmd = classproperty(lambda cls: cls.name[0])

    # The next command, this is for automatic chains where the next command
    # isn't given, just a bunch on numbers which we automatically parse.
    next_cmd = classproperty(lambda cls: (cls.this_cmd, cls.this_cmd.lower()))

    # Returns True/False if the command is relative/absolute
    # based on the case of the command
    isrelative = lambda self: self.cmd.islower()
    isabsolute = lambda self: self.cmd.isupper()

    # The precision of the numbers when converting to string
    number_template = "{:.6g}"

    @classmethod
    def __new__(cls, _, cmd, *args):
        if cmd.upper().strip() == cls.this_cmd:
            if len(args) < cls.num:
                raise InvalidPath("Bad arguments {}({})".format(cmd, args))
            obj = tuple.__new__(cls, args[:cls.num])
            obj.cmd = cmd
            if len(args) > cls.num:
                # pylint: disable=no-value-for-parameter
                nxt = PathCommand(cls.next_cmd[obj.cmd.islower()], *args[cls.num:])
                return [obj] + nxt if isinstance(nxt, list) else [obj, nxt]
            return obj
        try:
            return next(iter(filter(NONE, [c(cmd, *args) for c in cls.__subclasses__()])))
        except StopIteration:
            if cls is PathCommand:
                raise InvalidPath("Path command {} not recognised.".format(cmd))

    _argt = classmethod(lambda cls, sep: (sep + cls.number_template) * cls.num)

    def __str__(self):
        return self.cmd + self._argt(" ").format(*self)

    def __repr__(self):
        return "{{}}('{{}}'{})".format(self._argt(", ")).format(self.name, self.cmd, *self)

    def __add__(self, other):
        if self.isabsolute():
            return self.translate(other)
        return self

    def __mul__(self, other):
        return self.scale(other)

    all_x = property(lambda self: self[::2])
    all_y = property(lambda self: self[1::2])

    @property
    def points(self):
        """Returns a list of points in this path command, x and y only"""
        return tuple(zip(self.all_x, self.all_y))

    def bounding_box(self, prev):
        """Returns a rough bounding box, similar to roughBBox returns: (x1, x2, y1, y2)"""
        return BoundingBox(Scale(*self.all_x), Scale(*self.all_y))

    def translate(self, coords, opr=add):
        """Translate or scale this path command by the given coords X/Y"""
        lst = (opr(val, coords[i % 2]) for i, val in enumerate(self))
        return PathCommand(self.cmd, *lst)

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
        return PathCommand(self.cmd, *ans)

    def transform(self, transform, raw=False):
        """Apply a matrix transform to this path and return a new path"""
        transform = Transform(transform)
        points = list(self.points)
        for index, (x, y) in enumerate(points):
            points[index] = transform.apply_to_point([x, y])
        if raw:
            return points
        return PathCommand(self.cmd, *[coord for point in points for coord in point])

    def get_pen(self, previous=(0, 0)):
        """Where will the pen be after this command"""
        if not self.isabsolute():
            self = self.translate(previous)
        if self.num:
            return self.points[-1]
        return previous


class Line(PathCommand):
    """Line instruction"""
    num = 2


class ZClose(PathCommand):
    """Close instruction to finish a path"""
    next_cmd = 'Ll'
    num = 0


class Move(PathCommand):
    """Move pen instruction without a line"""
    next_cmd = 'Ll'
    num = 2


class Horz(PathCommand):
    """Horizontal Line instruction"""
    num = 1
    index = X
    points = property(lambda self: ((self[0], None),))

    def get_pen(self, previous):
        """When getting the pen for Horz moves, we return the combined point"""
        pen = super(Horz, self).get_pen(previous)
        return tuple(pen[i] is None and previous[i] or pen[i] for i in (0, 1))

    def translate(self, coords, opr=add):
        """Translate this Horz path by the given coords X/Y"""
        return PathCommand(self.cmd, opr(self[0], coords[self.index]))

    def transform(self, transform):
        raise ValueError("Hozontal lines can't be transformed directly.")

    def to_line(self, previous):
        """Return this path command as a line instead"""
        return PathCommand('L', self[0], previous[1])


class Vert(Horz):
    """Vertical Line instruction"""
    index = Y
    points = property(lambda self: ((None, self[0]),))

    all_x = property(lambda self: [])
    all_y = property(lambda self: self[:1])

    def to_line(self, previous):
        """Return this path command as a line instead"""
        return PathCommand('L', previous[0], self[0])


class Curve(PathCommand):
    """Curved Line instruction"""
    num = 6


class SmoothCurve(PathCommand):
    """Smoothed Curved Line instruction"""
    num = 4

    def bounding_box(self, prev):
        """Returns a bounding box for curved lines, similar to refinedBBox"""
        raise NotImplementedError("This requires the previous coords too")
        return cubic_extrema(*self.all_x) + cubic_extrema(*self.all_y)


class Quadratic(PathCommand):
    """Quadratic Curved Line instruction"""
    num = 4

    def bounding_box(self, prev):
        """Returns a bounding box for curved lines, similar to refinedBBox"""
        raise NotImplementedError("This requires the previous coords too")
        #return cubic_extrema(*self.all_y) + cubic_extrema(*self.all_y)


class TepidQuadratic(PathCommand):
    """Smoothed Quadratic Line instruction"""
    num = 2


class Arc(PathCommand):
    """Special Arc instruction"""
    num = 7
    points = property(lambda self: (self[-2:],))

    def bounding_box(self, prev):
        """Returns a bounding box for curved lines, similar to refinedBBox"""
        bbox = BoundingBox(None)
        for seg in self.to_curves(prev.get_pen()):
            bbox += seg.bounding_box(prev)
            prev = seg
        return bbox

    def to_curves(self, previous=(0, 0)):
        """Convert this arc into bezier curves"""
        cubic = ArcToPath(list(previous), list(self))
        for seg in unCubicSuperPath([cubic]):
            yield PathCommand(seg[0], *seg[1])

    def translate(self, coords, opr=add):
        """Translate or scale this path command by the given coords X/Y"""
        lst = self[:5] + (opr(self[5], coords[X]), opr(self[6], coords[Y]))
        return PathCommand(self.cmd, *lst)

    def transform(self, transform):
        """Transform this arc along with the given transformation"""
        points = super(Arc, self).transform(transform, raw=True)[0]
        return PathCommand(self.cmd, *(self[:-2] + tuple(points)))

    def scale(self, coords):
        """Scale the Arc by the given coords"""
        (x, y) = coords  # pylint: disable=invalid-name
        return PathCommand(self.cmd,
                           self[0] * x,  # Radius
                           self[1] * x,  # Radius
                           (self[2], 0)[y < 0],  # X-axis rotation angle
                           self[3],  # Unknown param '0'
                           (self[4], 1 - self[4])[x * y < 0],  # sweep-flag
                           self[5] * x,  # X coord
                           self[6] * y,  # Y coord
                           )


class Path(list):
    """A list of segment commands which combine to draw a shape"""

    def __init__(self, path_d=None):
        super(Path, self).__init__()
        if isinstance(path_d, str):
            for cmd, nums in LEX_REX.findall(path_d):
                self.append(PathCommand(cmd, *strargs(nums)))
        elif isinstance(path_d, (list, tuple)):
            for item in path_d:
                if isinstance(item, PathCommand):
                    self.append(item)
                elif isinstance(item, (list, tuple)) and len(item) == 2:
                    self.append(PathCommand(item[0], *item[1]))

    def bounding_box(self):
        """Return the top,left and bottom,right coords"""
        return sum([seg.bounding_box(prev) \
            for prev, seg in pairwise(self.to_absolute(curves=True)) \
                if seg])

    def append(self, cmd):
        """Append a command to this path including any chained commands"""
        if isinstance(cmd, list):
            self.extend(cmd)
        elif isinstance(cmd, PathCommand):
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
                segs = [PathCommand(
                    seg.cmd.swapcase(),
                    *seg.translate((pen[0] * factor, pen[1] * factor)))]
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
        return [[seg.cmd, list(seg)] for seg in self.to_absolute()]

    def copy(self):
        """Make a copy"""
        return copy.copy(self)
