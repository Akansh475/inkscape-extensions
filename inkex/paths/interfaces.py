# coding=utf-8
#
# Copyright (C) 2018 Martin Owens <doctormo@gmail.com>
# Copyright (C) 2023 Jonathan Neuhauser <jonathan.neuhauser@outlook.com>
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
"""Interfaces for path commands"""

from __future__ import annotations

import abc
from typing import List, Any, Tuple, Dict, Type, Generator, Union, TYPE_CHECKING

from ..utils import classproperty
from ..transforms import Vector2d, BoundingBox, Transform

if TYPE_CHECKING:
    from .curves import Curve
    from .lines import Line


class PathCommand(abc.ABC):
    """
    Base class of all path commands
    """

    letter = ""
    # Number of arguments that follow this path commands letter
    nargs = -1

    @classproperty  # From python 3.9 on, just combine @classmethod and @property
    def name(cls):  # pylint: disable=no-self-argument
        """The full name of the segment (i.e. Line, Arc, etc)"""
        return cls.__name__  # pylint: disable=no-member

    @classproperty
    def next_command(self):
        """The implicit next command. This is for automatic chains where the next
        command isn't given, just a bunch on numbers which we automatically parse."""
        return self

    @property
    def is_relative(self) -> bool:
        """Whether the command is defined in relative coordinates, i.e. relative to
        the previous endpoint (lower case path command letter)"""
        raise NotImplementedError

    @property
    def is_absolute(self) -> bool:
        """Whether the command is defined in absolute coordinates (upper case path
        command letter)"""
        raise NotImplementedError

    def to_relative(self, prev: complex) -> RelativePathCommand:
        """Return absolute counterpart for absolute commands or copy for relative"""
        raise NotImplementedError

    def to_absolute(self, prev: complex) -> AbsolutePathCommand:
        """Return relative counterpart for relative commands or copy for absolute"""
        raise NotImplementedError

    def reverse(self, first, prev):
        """Reverse path command

        .. versionadded:: 1.1"""

    def to_non_shorthand(
        self, prev: complex, prev_control: complex  # pylint: disable=unused-argument
    ) -> AbsolutePathCommand:
        """Return an absolute non-shorthand command

        .. versionadded:: 1.1"""
        return self.to_absolute(prev)

    # The precision of the numbers when converting to string
    number_template = "{:.6g}"

    # Maps single letter path command to corresponding class
    # (filled at the bottom of file, when all classes already defined)
    _letter_to_class: Dict[str, Type[Any]] = {}

    @staticmethod
    def letter_to_class(letter):
        """Returns class for given path command letter"""
        return PathCommand._letter_to_class[letter]

    @property
    @abc.abstractmethod
    def args(self) -> List[float]:
        """Returns path command arguments as tuple of floats"""

    def control_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Generator[Vector2d, None, None]:
        """Returns list of path command control points"""
        yield from [Vector2d(i) for i in self.ccontrol_points(first, prev, prev_prev)]

    @abc.abstractmethod
    def ccontrol_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        """Returns list of path command control points"""

    @classmethod
    def _argt(cls, sep):
        return sep.join([cls.number_template] * cls.nargs)

    def __str__(self):
        return f"{self.letter} {self._argt(' ').format(*self.args)}".strip()

    def __repr__(self):
        # pylint: disable=consider-using-f-string
        return "{{}}({})".format(self._argt(", ")).format(self.name, *self.args)

    def __eq__(self, other):
        previous = 0j
        if type(self) == type(other):  # pylint: disable=unidiomatic-typecheck
            return self.args == other.args
        if isinstance(other, tuple):
            return self.args == other
        if not isinstance(other, PathCommand):
            raise ValueError("Can't compare types")
        try:
            if self.is_relative == other.is_relative:
                return self.to_curve(previous) == other.to_curve(previous)
        except ValueError:
            pass
        return False

    @abc.abstractmethod
    def cend_point(self, first: complex, prev: complex) -> complex:
        """Complex version of end_point"""

    def end_point(self, first: complex, prev: complex) -> Vector2d:
        """Returns last control point of path command"""
        return Vector2d(self.cend_point(first, prev))

    @abc.abstractmethod
    def update_bounding_box(
        self, first: complex, last_two_points: List[complex], bbox: BoundingBox
    ):
        """Enlarges given bbox to contain path element.

        Args:
            first (complex): first point of path. Required to calculate Z segment
            last_two_points (List[complex]): list with last two control points in abs
                coords.
            bbox (BoundingBox): bounding box to update
        """

    def to_curve(self, prev: complex, prev_prev: complex = 0) -> Curve:
        # pylint: disable=unused-argument
        """Convert command to :py:class:`Curve`

        Curve().to_curve() returns a copy
        """
        return NotImplemented

    def to_curves(self, prev: complex, prev_prev: complex = 0) -> List[Curve]:
        """Convert command to list of :py:class:`Curve` commands"""
        return [self.to_curve(prev, prev_prev)]

    def to_line(self, prev: complex) -> Line:
        # pylint: disable=unused-argument
        """Converts this segment to a line (copies if already a line)"""
        return NotImplemented

    @abc.abstractmethod
    def ccurve_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        # pylint: disable=unused-argument
        """Converts the path element into a single cubic bezier"""


class RelativePathCommand(PathCommand):
    """
    Abstract base class for relative path commands.

    Implements most of methods of :py:class:`PathCommand` through
    conversion to :py:class:`AbsolutePathCommand`
    """

    @property
    def is_relative(self):
        return True

    @property
    def is_absolute(self):
        return False

    def to_relative(self, prev: complex) -> RelativePathCommand:
        return self.__class__(*self.args)

    def update_bounding_box(self, first, last_two_points, bbox):
        self.to_absolute(last_two_points[-1]).update_bounding_box(
            first, last_two_points, bbox
        )


class AbsolutePathCommand(PathCommand):
    """Absolute path command. Unlike :py:class:`RelativePathCommand` can be transformed
    directly."""

    @property
    def is_relative(self):
        return False

    @property
    def is_absolute(self):
        return True

    def to_absolute(self, prev: complex) -> AbsolutePathCommand:
        return self.__class__(*self.args)

    @abc.abstractmethod
    def transform(self, transform: Transform) -> AbsolutePathCommand:
        """Returns new transformed segment

        :param transform: a transformation to apply
        """

    def rotate(self, degrees: float, center: Vector2d) -> AbsolutePathCommand:
        """
        Returns new transformed segment

        :param degrees: rotation angle in degrees
        :param center: invariant point of rotation
        """
        return self.transform(Transform(rotate=(degrees, center[0], center[1])))

    def translate(self, dr: Vector2d) -> AbsolutePathCommand:
        """Translate or scale this path command by dr"""
        return self.transform(Transform(translate=dr))

    def scale(self, factor: Union[float, Tuple[float, float]]) -> AbsolutePathCommand:
        """Returns new transformed segment

        :param factor: scale or (scale_x, scale_y)
        """
        return self.transform(Transform(scale=factor))
