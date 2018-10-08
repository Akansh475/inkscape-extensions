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
"""Deprecated bezmisc API"""

from inkex.deprecated import deprecate
from inkex import bezier

bezierparameterize = deprecate(bezier.bezierparameterize)
linebezierintersect = deprecate(bezier.linebezierintersect)
bezierpointatt = deprecate(bezier.bezierpointatt)
bezierslopeatt = deprecate(bezier.bezierslopeatt)
beziertatslope = deprecate(bezier.beziertatslope)
tpoint = deprecate(bezier.tpoint)
beziersplitatt = deprecate(bezier.beziersplitatt)
pointdistance = deprecate(bezier.pointdistance)
Gravesen_addifclose = deprecate(bezier.Gravesen_addifclose)
bezierlengthGravesen = deprecate(bezier.bezierlengthGravesen)
balf = deprecate(bezier.balf)
Simpson = deprecate(bezier.Simpson)
bezierlengthSimpson = deprecate(bezier.bezierlengthSimpson)
beziertatlength = deprecate(bezier.beziertatlength)
bezierlength = bezierlengthSimpson
