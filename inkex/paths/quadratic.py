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
"""Quadratic and TepidQuadratic path commands"""

from __future__ import annotations

from typing import overload, Tuple

from ..transforms import quadratic_extrema, Transform

from .interfaces import AbsolutePathCommand, RelativePathCommand


class Quadratic(AbsolutePathCommand):
    """Absolute Quadratic Curved Line segment"""

    letter = "Q"
    nargs = 4

    arg1: complex
    """The (absolute) control point"""

    arg2: complex
    """The (absolute) end point"""

    @property
    def x2(self) -> float:
        """x coordinate of the (absolute) control point"""
        return self.arg1.real

    @property
    def y2(self) -> float:
        """y coordinate of the (absolute) control point"""
        return self.arg1.imag

    @property
    def x3(self) -> float:
        """x coordinate of the (absolute) end point"""
        return self.arg2.real

    @property
    def y3(self) -> float:
        """y coordinate of the (absolute) end point"""
        return self.arg2.imag

    @property
    def args(self):
        return self.x2, self.y2, self.x3, self.y3

    @overload
    def __init__(self, x2: complex, x3: complex):
        ...

    @overload
    def __init__(self, x2: float, y2: float, x3: float, y3: float):
        ...

    def __init__(self, x2, y2, x3=None, y3=None):
        if x3 is not None:
            self.arg1 = x2 + y2 * 1j
            self.arg2 = x3 + y3 * 1j
        else:
            self.arg1, self.arg2 = x2, y2

    def update_bounding_box(self, first, last_two_points, bbox):
        x1, x2, x3 = last_two_points[-1].real, self.x2, self.x3
        y1, y2, y3 = last_two_points[-1].imag, self.y2, self.y3

        if not (x1 in bbox.x and x2 in bbox.x and x3 in bbox.x):
            bbox.x += quadratic_extrema(x1, x2, x3)

        if not (y1 in bbox.y and y2 in bbox.y and y3 in bbox.y):
            bbox.y += quadratic_extrema(y1, y2, y3)

    def ccontrol_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return (self.arg1, self.arg2)

    def to_relative(self, prev: complex) -> quadratic:
        return quadratic(self.arg1 - prev, self.arg2 - prev)

    def transform(self, transform: Transform) -> Quadratic:
        return Quadratic(
            transform.capply_to_point(self.arg1), transform.capply_to_point(self.arg2)
        )

    def cend_point(self, first: complex, prev: complex) -> complex:
        return self.arg2

    def ccurve_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        pt1 = 1.0 / 3 * prev + 2.0 / 3 * self.arg1
        pt2 = 2.0 / 3 * self.arg1 + 1.0 / 3 * self.arg2
        return pt1, pt2, self.arg2

    def reverse(self, first, prev):
        return Quadratic(self.x2, self.y2, prev.x, prev.y)


class quadratic(RelativePathCommand):  # pylint: disable=invalid-name
    """Relative quadratic line segment"""

    letter = "q"
    nargs = 4

    arg1: complex
    """The (relative) control point"""

    arg2: complex
    """The (relative) end point"""

    @property
    def dx2(self) -> float:
        """x coordinate of the (relative) control point"""
        return self.arg1.real

    @property
    def dy2(self) -> float:
        """y coordinate of the (relative) control point"""
        return self.arg1.imag

    @property
    def dx3(self) -> float:
        """x coordinate of the (relative) end point"""
        return self.arg2.real

    @property
    def dy3(self) -> float:
        """y coordinate of the (relative) end point"""
        return self.arg2.imag

    @property
    def args(self):
        return self.dx2, self.dy2, self.dx3, self.dy3

    @overload
    def __init__(self, dx2: complex, dx3: complex):
        ...

    @overload
    def __init__(self, dx2: float, dy2: float, dx3: float, dy3: float):
        ...

    def __init__(self, dx2, dy2, dx3=None, dy3=None):
        if dx3 is not None:
            self.arg1 = dx2 + dy2 * 1j
            self.arg2 = dx3 + dy3 * 1j
        else:
            self.arg1, self.arg2 = dx2, dy2

    def ccontrol_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return (self.arg1 + prev, self.arg2 + prev)

    def to_absolute(self, prev: complex) -> Quadratic:
        return Quadratic(self.arg1 + prev, self.arg2 + prev)

    def ccurve_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        pt1 = 1.0 / 3 * prev + 2.0 / 3 * (prev + self.arg1)
        pt2 = 2.0 / 3 * (prev + self.arg1) + 1.0 / 3 * (prev + self.arg2)
        return pt1, pt2, prev + self.arg2

    def cend_point(self, first: complex, prev: complex) -> complex:
        return self.arg2 + prev

    def reverse(self, first: complex, prev: complex) -> quadratic:
        return quadratic(-self.arg2 + self.arg1, -self.arg2)


class TepidQuadratic(AbsolutePathCommand):
    """Continued Quadratic Line segment"""

    letter = "T"
    nargs = 2

    arg1: complex
    """The (absolute) control point"""

    @property
    def x3(self) -> float:
        """x coordinate of the (absolute) end point"""
        return self.arg1.real

    @property
    def y3(self) -> float:
        """y coordinate of the (absolute) end point"""
        return self.arg1.imag

    @property
    def args(self):
        return self.x3, self.y3

    @overload
    def __init__(self, x3: complex):
        ...

    @overload
    def __init__(self, x3: float, y3: float):
        ...

    def __init__(self, x3, y3=None):
        if y3 is not None:
            self.arg1 = x3 + y3 * 1j
        else:
            self.arg1 = x3

    def update_bounding_box(self, first, last_two_points, bbox):
        self.to_quadratic(last_two_points[-1], last_two_points[-2]).update_bounding_box(
            first, last_two_points, bbox
        )

    def ccontrol_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return (2 * prev - prev_prev, self.arg1)

    def to_non_shorthand(self, prev: complex, prev_control: complex) -> Quadratic:
        return self.to_quadratic(prev, prev_control)

    def to_relative(self, prev: complex) -> tepidQuadratic:
        return tepidQuadratic(self.arg1 - prev)

    def transform(self, transform: Transform) -> TepidQuadratic:
        return TepidQuadratic(transform.capply_to_point(self.arg1))

    def ccurve_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        qp1 = 2 * prev - prev_prev
        qp2 = self.arg1
        pt1 = 1.0 / 3 * prev + 2.0 / 3 * qp1
        pt2 = 2.0 / 3 * qp1 + 1.0 / 3 * qp2
        return pt1, pt2, qp2

    def cend_point(self, first: complex, prev: complex) -> complex:
        return self.arg1

    def to_quadratic(self, prev: complex, prev_prev: complex) -> Quadratic:
        """Convert this continued quadratic into a full quadratic"""
        return Quadratic(*self.ccontrol_points(prev, prev, prev_prev))

    def reverse(self, first: complex, prev: complex) -> TepidQuadratic:
        return TepidQuadratic(prev)


class tepidQuadratic(RelativePathCommand):  # pylint: disable=invalid-name
    """Relative continued quadratic line segment"""

    letter = "t"
    nargs = 2

    arg1: complex
    """The (relative) control point"""

    @property
    def dx3(self) -> float:
        """x coordinate of the (relative) end point"""
        return self.arg1.real

    @property
    def dy3(self) -> float:
        """y coordinate of the (relative) end point"""
        return self.arg1.imag

    @property
    def args(self):
        return self.dx3, self.dy3

    @overload
    def __init__(self, dx3: complex):
        ...

    @overload
    def __init__(self, dx3: float, dy3: float):
        ...

    def __init__(self, dx3, dy3=None):
        if dy3 is not None:
            self.arg1 = dx3 + dy3 * 1j
        else:
            self.arg1 = dx3

    def ccontrol_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return (2 * prev - prev_prev, self.arg1 + prev)

    def ccurve_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        qp1 = 2 * prev - prev_prev
        qp2 = self.arg1 + prev
        pt1 = 1.0 / 3 * prev + 2.0 / 3 * qp1
        pt2 = 2.0 / 3 * qp1 + 1.0 / 3 * qp2
        return pt1, pt2, qp2

    def to_absolute(self, prev: complex) -> TepidQuadratic:
        return TepidQuadratic(self.arg1 + prev)

    def to_non_shorthand(self, prev: complex, prev_control: complex) -> Quadratic:
        return self.to_absolute(prev).to_non_shorthand(prev, prev_control)

    def cend_point(self, first: complex, prev: complex) -> complex:
        return self.arg1 + prev

    def reverse(self, first: complex, prev: complex) -> tepidQuadratic:
        return tepidQuadratic(-self.arg1)
