# coding=utf-8
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
# pylint: disable=invalid-name
"""Deprecated cubic super path API"""

from inkex.deprecated import deprecate
from inkex import cubic_paths

matprod = deprecate(cubic_paths.matprod)
rotmat = deprecate(cubic_paths.rotmat)
applymat = deprecate(cubic_paths.applymat)
norm = deprecate(cubic_paths.norm)
ArcToPath = deprecate(cubic_paths.ArcToPath)
CubicSuperPath = deprecate(cubic_paths.CubicSuperPath)
unCubicSuperPath = deprecate(cubic_paths.unCubicSuperPath)
parsePath = deprecate(cubic_paths.parseCubicPath)
formatPath = deprecate(cubic_paths.formatCubicPath)

