#!/usr/bin/env python
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

import inkex

DOCNAME = 'sodipodi:docname'
TAGS = ('fill', 'stroke', 'stop-color', 'flood-color', 'lighting-color')

class ExportGpl(inkex.Effect):
    def effect(self):
        svg = self.document.getroot()

        print('GIMP Palette\nName: %s\n#' % (svg.get(inkex.addNS("docname", "sodipodi"))))
        colors = dict(self.walk(svg))
        for key, value in sorted(colors.items()):
            print(key + value)

    def walk(self, node):
        """Walks over all svg dom nodes"""
        styles = dict(inkex.Style.parse_str(node.get('style', '')))
        for tag in TAGS:
            col = styles.get(tag, None)
            if col is not None and inkex.is_color(col):
                parsed = inkex.Color(col).to_rgb()
                yield ('%3i %3i %3i ' % tuple(parsed[:3]), str(parsed).upper())

        for child in node.iterchildren():
            for color in self.walk(child):
                yield color

if __name__ == '__main__':
    ExportGpl().affect()


