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
"""Arc path commands"""


from __future__ import annotations
from math import atan2, pi, sqrt, sin, cos, tan, acos
from typing import overload, Tuple, List, TYPE_CHECKING

from ..transforms import Transform

from .interfaces import AbsolutePathCommand, RelativePathCommand

if TYPE_CHECKING:
    from .curves import Curve


class Arc(AbsolutePathCommand):
    """Special Arc segment"""

    letter = "A"

    nargs = 7

    radius: complex
    """Radius of the Arc"""
    x_axis_rotation: float

    large_arc: bool
    sweep: bool

    endpoint: complex
    """Endpoint (absolute) of the Arc"""

    @property
    def rx(self) -> float:
        """x radius of the Arc"""
        return self.radius.real

    @property
    def ry(self) -> float:
        """y radius of the Arc"""
        return self.radius.imag

    @property
    def x(self) -> float:
        """x coordinate of the (absolute) endpoint of the Arc"""
        return self.endpoint.real

    @property
    def y(self) -> float:
        """x coordinate of the (relative) endpoint of the Arc"""
        return self.endpoint.imag

    @property
    def args(self):
        return (
            self.rx,
            self.ry,
            self.x_axis_rotation,
            self.large_arc,
            self.sweep,
            self.x,
            self.y,
        )

    @property
    def cargs(self):
        """Set of arguments in complex form"""
        return (
            self.radius,
            self.x_axis_rotation,
            self.large_arc,
            self.sweep,
            self.endpoint,
        )

    @overload
    def __init__(
        self,
        radius: complex,
        x_axis_rotation: float,
        large_arc: bool | int,
        sweep: bool | int,
        endpoint: complex,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        rx: float,
        ry: float,
        x_axis_rotation: float,
        large_arc: bool | int,
        sweep: bool | int,
        x: float,
        y: float,
    ) -> None:
        ...  # pylint: disable=too-many-arguments

    def __init__(self, *args):
        if len(args) == 5:
            (
                self.radius,
                self.x_axis_rotation,
                self.large_arc,
                self.sweep,
                self.endpoint,
            ) = args
        elif len(args) == 7:
            self.radius = args[0] + args[1] * 1j
            self.x_axis_rotation, self.large_arc, self.sweep = args[2:5]
            self.endpoint = args[5] + args[6] * 1j

    def update_bounding_box(self, first, last_two_points, bbox):
        prev = last_two_points[-1]
        for seg in self.to_curves(prev=prev):
            seg.update_bounding_box(first, [None, prev], bbox)
            prev = seg.cend_point(first, prev)

    def ccontrol_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return (self.endpoint,)

    def ccurve_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return NotImplemented

    def to_curves(self, prev: complex, prev_prev: complex = 0j) -> List[Curve]:
        """Convert this arc into bezier curves"""
        # TODO Refactor out CubicSuperPath
        from .path import CubicSuperPath

        path = CubicSuperPath([arc_to_path([prev.real, prev.imag], self.args)]).to_path(
            curves_only=True
        )
        # Ignore the first move command from to_path()
        return list(path)[1:]

    def transform(self, transform: Transform) -> Arc:
        # pylint: disable=invalid-name, too-many-locals
        newend = transform.capply_to_point(self.endpoint)

        T: Transform = transform
        if self.x_axis_rotation != 0:
            T = T @ Transform(rotate=self.x_axis_rotation)
        a, c, b, d, _, _ = list(T.to_hexad())
        # T = | a b |
        #     | c d |

        detT = a * d - b * c
        detT2 = detT**2

        rx = float(self.rx)
        ry = float(self.ry)

        if rx == 0.0 or ry == 0.0 or detT2 == 0.0:
            # invalid Arc parameters
            # transform only last point
            return Arc(
                self.radius,
                self.x_axis_rotation,
                self.large_arc,
                self.sweep,
                newend,
            )

        A = (d**2 / rx**2 + c**2 / ry**2) / detT2
        B = -(d * b / rx**2 + c * a / ry**2) / detT2
        D = (b**2 / rx**2 + a**2 / ry**2) / detT2

        theta = atan2(-2 * B, D - A) / 2
        theta_deg = theta * 180.0 / pi
        DA = D - A
        l2 = 4 * B**2 + DA**2

        if l2 == 0:
            delta = 0.0
        else:
            delta = 0.5 * (-(DA**2) - 4 * B**2) / sqrt(l2)

        half = (A + D) / 2

        rx_ = 1.0 / sqrt(half + delta)
        ry_ = 1.0 / sqrt(half - delta)

        if detT > 0:
            sweep = self.sweep
        else:
            sweep = not self.sweep > 0

        return Arc(rx_ + 1j * ry_, theta_deg, self.large_arc, sweep, newend)

    def to_relative(self, prev: complex) -> arc:
        return arc(
            self.radius,
            self.x_axis_rotation,
            self.large_arc,
            self.sweep,
            self.endpoint - prev,
        )

    def cend_point(self, first: complex, prev: complex) -> complex:
        return self.endpoint

    def reverse(self, first: complex, prev: complex) -> Arc:
        return Arc(
            self.radius, self.x_axis_rotation, self.large_arc, not self.sweep, prev
        )


class arc(RelativePathCommand):  # pylint: disable=invalid-name
    """Relative Arc line segment"""

    letter = "a"

    nargs = 7

    radius: complex
    """Radius of the arc"""
    x_axis_rotation: float

    large_arc: bool
    sweep: bool

    endpoint: complex
    """Endpoint (relative) of the arc"""

    @property
    def rx(self) -> float:
        """x radius of the arc"""
        return self.radius.real

    @property
    def ry(self) -> float:
        """y radius of the arc"""
        return self.radius.imag

    @property
    def dx(self) -> float:
        """x coordinate of the (relative) endpoint of the arc"""
        return self.endpoint.real

    @property
    def dy(self) -> float:
        """x coordinate of the (relative) endpoint of the arc"""
        return self.endpoint.imag

    @property
    def args(self):
        return (
            self.rx,
            self.ry,
            self.x_axis_rotation,
            self.large_arc,
            self.sweep,
            self.dx,
            self.dy,
        )

    @overload
    def __init__(
        self,
        radius: complex,
        x_axis_rotation: float,
        large_arc: bool,
        sweep: bool,
        endpoint: complex,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        rx: float,
        ry: float,
        x_axis_rotation: float,
        large_arc: bool,
        sweep: bool,
        dx: float,
        dy: float,
    ) -> None:
        ...  # pylint: disable=too-many-arguments

    def __init__(self, *args):
        if len(args) == 5:
            (
                self.radius,
                self.x_axis_rotation,
                self.large_arc,
                self.sweep,
                self.endpoint,
            ) = args
        elif len(args) == 7:
            self.radius = args[0] + args[1] * 1j
            self.x_axis_rotation, self.large_arc, self.sweep = args[2:5]
            self.endpoint = args[5] + args[6] * 1j

    def to_absolute(self, prev: complex) -> Arc:
        return Arc(
            self.radius,
            self.x_axis_rotation,
            self.large_arc,
            self.sweep,
            self.endpoint + prev,
        )

    def cend_point(self, first: complex, prev: complex) -> complex:
        return self.endpoint + prev

    def ccontrol_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return (self.endpoint + prev,)

    def ccurve_points(
        self, first: complex, prev: complex, prev_prev: complex
    ) -> Tuple[complex, ...]:
        return NotImplemented

    def reverse(self, first: complex, prev: complex) -> arc:
        return arc(
            self.radius,
            self.x_axis_rotation,
            self.large_arc,
            not self.sweep,
            -self.endpoint,
        )

    def to_curves(self, prev: complex, prev_prev: complex = 0j) -> List[Curve]:
        return self.to_absolute(prev).to_curves(prev, prev_prev)


def arc_to_path(point, params):
    """Approximates an arc with cubic bezier segments.

    Arguments:
        point:  Starting point (absolute coords)
        params: Arcs parameters as per
              https://www.w3.org/TR/SVG/paths.html#PathDataEllipticalArcCommands

    Returns a list of triplets of points :
    [control_point_before, node, control_point_after]
    (first and last returned triplets are [p1, p1, *] and [*, p2, p2])
    """

    # pylint: disable=invalid-name, too-many-locals
    A = point[:]
    rx, ry, teta, longflag, sweepflag, x2, y2 = params[:]
    teta = teta * pi / 180.0
    B = [x2, y2]
    # Degenerate ellipse
    if rx == 0 or ry == 0 or A == B:
        return [[A[:], A[:], A[:]], [B[:], B[:], B[:]]]

    # turn coordinates so that the ellipse morph into a *unit circle* (not 0-centered)
    mat = matprod((rotmat(teta), [[1.0 / rx, 0.0], [0.0, 1.0 / ry]], rotmat(-teta)))
    applymat(mat, A)
    applymat(mat, B)

    k = [-(B[1] - A[1]), B[0] - A[0]]
    d = k[0] * k[0] + k[1] * k[1]
    k[0] /= sqrt(d)
    k[1] /= sqrt(d)
    d = sqrt(max(0, 1 - d / 4.0))
    # k is the unit normal to AB vector, pointing to center O
    # d is distance from center to AB segment (distance from O to the midpoint of AB)
    # for the last line, remember this is a unit circle, and kd vector is ortogonal to
    # AB (Pythagorean thm)

    if longflag == sweepflag:
        # top-right ellipse in SVG example
        # https://www.w3.org/TR/SVG/images/paths/arcs02.svg
        d *= -1

    O = [(B[0] + A[0]) / 2.0 + d * k[0], (B[1] + A[1]) / 2.0 + d * k[1]]
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
    v = 4 * tan(dTeta / 4.0) / 3.0
    # I would use v = tan(dTeta/2)*4*(sqrt(2)-1)/3 ?
    p = []
    for i in range(0, NbSectors + 1, 1):
        angle = start + i * dTeta
        v1 = [
            O[0] + cos(angle) - (-v) * sin(angle),
            O[1] + sin(angle) + (-v) * cos(angle),
        ]
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
