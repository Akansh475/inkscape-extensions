# coding=utf-8
#
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
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

import math

from bisect import bisect_left
from .utils import X, Y
from .units import convert_unit, parse_unit, render_unit

try:
    from typing import Tuple, List, TypeVar, Callable
    V = TypeVar('V')
except ImportError:
    pass


def interpcoord(coord_a, coord_b, time): # type: (float, float, float) -> float
    """Interpolate single coordinate by the amount of time"""
    return coord_a + ((coord_b - coord_a) * time)


def interp(positions, values, newpositions, func=None): # type: (Callable[[V, V, float], V], List[float], List[V], List[float]) -> V
    """Interpolate list with arbitrary interpolation function."""
    newvalues = []
    positions = list(map(float, positions))
    newpositions = list(map(float, newpositions))
    for pos in newpositions:
        idxl = max(0, bisect_left(positions, pos) - 1)
        idxr = min(len(positions)-1, idxl + 1)
        fraction = (pos - positions[idxl]) / (positions[idxr] - positions[idxl])
        vall = values[idxl]
        valr = values[idxr]
        if func is not None:
            newval = func(vall, valr, fraction)
        if isinstance(vall, (float, int)):
            newval = interpcoord(vall, valr, fraction)
        elif hasattr(vall, 'interpolate'):
            newval = vall.interpolate(valr, fraction)
        else:
            raise Exception('Interpolated objects must be float/int or have an interpolate method if func is not passed as argument')
        newvalues.append(newval)
    return newvalues


def interppoints(point1, point2, time): # type: (Tuple[float, float], Tuple[float, float], float) -> Tuple[float, float]
    """Interpolate coordinate points by amount of time"""
    return (interpcoord(point1[X], point2[X], time), interpcoord(point1[Y], point2[Y], time))


def interpunit(start, end, fraction): # type: (SvgDocumentElement, str, str, str, float) -> str
    """Interpolate float attributes with unit."""
    # moved here so we can call 'unittouu'
    sp, unit = parse_unit(start)
    ep = convert_unit(end, unit)
    return render_unit(interpcoord(sp, ep, fraction), unit)
