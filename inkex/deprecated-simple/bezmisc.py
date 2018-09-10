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
"""Depricated bezmisc API"""

from inkex.depricated import depricate
from inkex import bezier

bezierparameterize = depricate(bezier.bezierparameterize)
linebezierintersect = depricate(bezier.linebezierintersect)
bezierpointatt = depricate(bezier.bezierpointatt)
bezierslopeatt = depricate(bezier.bezierslopeatt)
beziertatslope = depricate(bezier.beziertatslope)
tpoint = depricate(bezier.tpoint)
beziersplitatt = depricate(bezier.beziersplitatt)
pointdistance = depricate(bezier.pointdistance)
Gravesen_addifclose = depricate(bezier.Gravesen_addifclose)
bezierlengthGravesen = depricate(bezier.bezierlengthGravesen)
balf = depricate(bezier.balf)
Simpson = depricate(bezier.Simpson)
bezierlengthSimpson = depricate(bezier.bezierlengthSimpson)
beziertatlength = depricate(bezier.beziertatlength)
bezierlength = bezierlengthSimpson
