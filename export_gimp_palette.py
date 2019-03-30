#!/usr/bin/env python
# coding=utf-8
#
# Copyright (c) 2009 - Jos Hirth, kaioa.com
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Export a gimp pallet file (.gpl)
"""

from __future__ import absolute_import, print_function, unicode_literals

from inkex.generic import OutputExtension
from inkex.colors import Color

DOCNAME = 'sodipodi:docname'
TAGS = ('fill', 'stroke', 'stop-color', 'flood-color', 'lighting-color')

class ExportGpl(OutputExtension):
    def save(self, stream):
        name = self.svg.name.replace('.svg', '')
        stream.write('GIMP Palette\nName: {}\n#\n'.format(name).encode('utf-8'))
        colors = dict(self.walk(self.svg))
        for key, value in sorted(colors.items()):
            stream.write("{} {}\n".format(key, value).encode('utf-8'))

    def walk(self, node):
        """Walks over all svg dom nodes"""
        styles = getattr(node, 'style', None) #dict(inkex.Style.parse_str(node.get('style', '')))
        for tag in TAGS:
            if styles and tag in styles:
                col = Color(styles.get(tag, None))
                if col:
                    yield ("{:3d} {:3d} {:3d}".format(*col.to_rgb()), str(str(col)).upper())

        for child in node:
            for color in self.walk(child):
                yield color

if __name__ == '__main__':
    ExportGpl().run()
