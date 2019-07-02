#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2005,2007 Aaron Spike, aaron@ekips.org
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
"""
Embed images so they are base64 encoded data inside the svg.
"""

from __future__ import unicode_literals

import os
import base64

import inkex
from inkex import inkbool
from inkex.localization import _
from inkex.elements import Image

try:
    import urllib.request as urllib
    import urllib.parse as urlparse
except ImportError:
    import urllib
    import urlparse

class Embedder(inkex.EffectExtension):
    """Allow selected image tags to become embeded image tags"""
    def add_arguments(self, pars):
        pars.add_argument("-s", "--selectedonly",
                          type=inkbool,
                          dest="selectedonly", default=False,
                          help="embed only selected images")

    def effect(self):
        # if slectedonly is enabled and there is a selection
        # only embed selected images. otherwise embed all images
        if self.options.selectedonly:
            images = self.svg.selected.values()
        else:
            images = self.svg.xpath('//svg:image')

        for node in images:
            if isinstance(node, Image):
                self.embed_image(node)

    def embed_image(self, node):
        """Embed the data of the selected Image Tag element"""
        xlink = node.get(inkex.addNS('href', 'xlink'))
        if xlink and xlink[:5] == 'data:':
            # No need, data alread embedded
            return

        absref = node.get(inkex.addNS('absref', 'sodipodi'))
        url = urlparse.urlparse(xlink)
        href = urllib.url2pathname(url.path)

        path = ''
        # path selection strategy:
        # 1. href if absolute
        # 2. realpath-ified href
        # 3. absref, only if the above does not point to a file
        if href is not None:
            path = os.path.realpath(href)

        if not os.path.isfile(path):
            if absref is not None:
                path = absref

        if not os.path.isfile(path):
            inkex.errormsg(_('No xlink:href or sodipodi:absref attributes found, or '\
                'they do not point to an existing file! Unable to embed image.'))
            if path:
                inkex.errormsg(_("Sorry we could not locate %s") % str(path))
            return

        with open(path, "rb") as handle:
            # Don't read the whole file to check the header
            file_type = self.get_type(path, handle.read(10))
            handle.seek(0)

            if file_type:
                # Future: Change encodestring to encodebytes when python3 only
                node.set('xlink:href', 'data:{};base64,{}'.format(
                    file_type, base64.encodestring(handle.read()).decode('ascii')))
                node.pop('sodipodi:absref')
            else:
                inkex.errormsg(_("%s is not of type image/png, image/jpeg, "\
                    "image/bmp, image/gif, image/tiff, or image/x-icon") % path)

    def get_type(self, path, header):
        """Basic magic header checker, returns mime type"""
        if header[:4] == b'\x89PNG':
            return 'image/png'
        elif header[:2] == b'\xff\xd8':
            return 'image/jpeg'
        elif header[:2] == b'BM':
            return 'image/bmp'
        elif header[:6] == b'GIF87a' or header[:6] == b'GIF89a':
            return 'image/gif'
        elif header[:4] == b'MM\x00\x2a' or header[:4] == b'II\x2a\x00':
            return 'image/tiff'
        # ico files lack any magic... therefore we check the filename instead
        elif path.endswith('.ico'):
            # official IANA registered MIME is 'image/vnd.microsoft.icon' tho
            return 'image/x-icon'
        elif path.endswith('.svg'):
            return 'image/svg+xml'
        return None

if __name__ == '__main__':
    Embedder().run()
