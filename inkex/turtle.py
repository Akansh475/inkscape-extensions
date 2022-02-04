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
import random
from typing import List, Union

from .paths import Line, Move, Path, PathCommand
from .elements import PathElement, Group
from .base import BaseElement
from .styles import Style


class pTurtle:
    """A Python path turtle"""

    def __init__(self, home=(0, 0)):
        self.__home = [home[0], home[1]]
        self.__pos = self.__home[:]
        self.__heading = -90
        self.__path = ""
        self.__draw = True
        self.__new = True

    def forward(self, mag):
        self.setpos(
            (
                self.__pos[0] + math.cos(math.radians(self.__heading)) * mag,
                self.__pos[1] + math.sin(math.radians(self.__heading)) * mag,
            )
        )

    def backward(self, mag):
        self.setpos(
            (
                self.__pos[0] - math.cos(math.radians(self.__heading)) * mag,
                self.__pos[1] - math.sin(math.radians(self.__heading)) * mag,
            )
        )

    def right(self, deg):
        self.__heading -= deg

    def left(self, deg):
        self.__heading += deg

    def penup(self):
        self.__draw = False
        self.__new = False

    def pendown(self):
        if not self.__draw:
            self.__new = True
        self.__draw = True

    def pentoggle(self):
        if self.__draw:
            self.penup()
        else:
            self.pendown()

    def home(self):
        self.setpos(self.__home)

    def clean(self):
        self.__path = ""

    def clear(self):
        self.clean()
        self.home()

    def setpos(self, arg):
        if self.__new:
            self.__path += "M" + ",".join([str(i) for i in self.__pos])
            self.__new = False
        self.__pos = arg
        if self.__draw:
            self.__path += "L" + ",".join([str(i) for i in self.__pos])

    def getpos(self):
        return self.__pos[:]

    def setheading(self, deg):
        self.__heading = deg

    def getheading(self):
        return self.__heading

    def sethome(self, arg):
        self.__home = list(arg)

    def getPath(self):
        return self.__path

    def rtree(self, size, minimum, pt=False):
        if size < minimum:
            return
        self.fd(size)
        turn = random.uniform(20, 40)
        self.lt(turn)
        self.rtree(size * random.uniform(0.5, 0.9), minimum, pt)
        self.rt(turn)
        turn = random.uniform(20, 40)
        self.rt(turn)
        self.rtree(size * random.uniform(0.5, 0.9), minimum, pt)
        self.lt(turn)
        if pt:
            self.pu()
        self.bk(size)
        if pt:
            self.pd()

    fd = forward
    bk = backward
    rt = right
    lt = left
    pu = penup
    pd = pendown


class PathBuilder:
    """This helper class can be used to construct a path and insert it into a document."""

    def __init__(self, style: Style):
        """Initializes a PathDrawHelper object

        Args:
            style (Style): Style of the path.
        """
        self.current = Path()
        self.style = style

    def add(self, command: Union[PathCommand, List[PathCommand]]):
        """Add a Path command to the Helper

        Args:
            command (Union[PathCommand, List[PathCommand]]): A (list of) PathCommand(s) to be
                                                             appended.
        """
        self.current.append(command)

    def terminate(self):
        """Terminates current subpath. This method does nothing by default and is supposed to be
        overridden in subclasses."""

    def append_next(self, sibling_before: BaseElement):
        """Insert the resulting Path as :class:`inkex.elements._polygons.PathElement`
        into the document tree.

        Args:
            sibling_before (BaseElement): The element the resulting path will be appended after.
        """
        pth = PathElement()
        pth.path = self.current
        pth.style = self.style
        sibling_before.addnext(pth)

    def Move_to(self, x, y):  # pylint: disable=invalid-name
        """Shorthand to insert an absolute move command: `M x y`.

        Args:
            x (Float): x coordinate to move to
            y (Float): y coordinate to move to
        """
        self.add(Move(x, y))

    def Line_to(self, x, y):  # pylint: disable=invalid-name
        """Shorthand to insert an absolute lineto command: `L x y`.

        Args:
            x (Float): x coordinate to draw a line to
            y (Float): y coordinate to draw a line to
        """
        self.add(Line(x, y))


class PathGroupBuilder(PathBuilder):
    """This helper class can be used to construct a group of paths that all have the same style."""

    def __init__(self, style):
        super().__init__(style)
        self.result = Group()

    def terminate(self):
        """Terminates the current Path, and appends it to the group if it is not empty."""
        if len(self.current) > 1:
            pth = PathElement()
            pth.path = self.current.to_absolute()
            pth.style = self.style
            self.result.append(pth)
        self.current = Path()

    def append_next(self, sibling_before: BaseElement):
        """Insert the resulting Path as :class:`inkex.elements._groups.Group` into the document tree.

        Args:
            sibling_before (BaseElement): The element the resulting group will be appended after.
        """
        sibling_before.addnext(self.result)
