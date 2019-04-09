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

from __future__ import unicode_literals

import base64
import os
import sys

import inkex
from inkex import inkbool
from inkex.generic import EffectExtension
from inkex.localize import _

if sys.version_info[0] == 2:
    import urllib
    import urlparse
else:
    import urllib.request as urllib
    import urllib.parse as urlparse


class Embedder(EffectExtension):
    def __init__(self):
        super(Embedder, self).__init__()
        self.arg_parser.add_argument("-s", "--selectedonly",
                                     type=inkbool,
                                     dest="selectedonly", default=False,
                                     help="embed only selected images")

    def effect(self):
        # if slectedonly is enabled and there is a selection only embed selected
        # images. otherwise embed all images
        if self.options.selectedonly:
            self.embedSelected(self.document, self.selected)
        else:
            self.embedAll(self.document)

    def embedSelected(self, document, selected):
        self.document = document
        self.selected = selected
        if self.options.ids:
            for id, node in selected.items():
                if node.tag == inkex.addNS('image', 'svg'):
                    self.embedImage(node)

    def embedAll(self, document):
        self.document = document  # not that nice... oh well
        path = '//svg:image'
        for node in self.document.getroot().xpath(path, namespaces=inkex.NSS):
            self.embedImage(node)

    def embedImage(self, node):
        xlink = node.get(inkex.addNS('href', 'xlink'))
        if xlink is None or xlink[:5] != 'data:':
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
                inkex.errormsg(_('No xlink:href or sodipodi:absref attributes found, or they do not point to an existing file! Unable to embed image.'))
                if path:
                    inkex.errormsg(_("Sorry we could not locate %s") % str(path))

            if os.path.isfile(path):
                with open(path, "rb").read() as f:
                    embed = True
                    if file[:4] == b'\x89PNG':
                        file_type = 'image/png'
                    elif file[:2] == b'\xff\xd8':
                        file_type = 'image/jpeg'
                    elif file[:2] == b'BM':
                        file_type = 'image/bmp'
                    elif file[:6] == b'GIF87a' or file[:6] == b'GIF89a':
                        file_type = 'image/gif'
                    elif file[:4] == b'MM\x00\x2a' or file[:4] == b'II\x2a\x00':
                        file_type = 'image/tiff'
                    # ico files lack any magic... therefore we check the filename instead
                    elif path.endswith('.ico'):
                        file_type = 'image/x-icon'  # official IANA registered MIME is 'image/vnd.microsoft.icon' tho
                    elif path.endswith('.svg'):
                        file_type = 'image/svg+xml'
                    else:
                        embed = False
                    if embed:
                        node.set(inkex.addNS('href', 'xlink'), 'data:{};base64,{}'.format(file_type, base64.encodestring(file).decode('ascii')))
                        if absref is not None:
                            del node.attrib[inkex.addNS('absref', u'sodipodi')]
                    else:
                        inkex.errormsg(_("%s is not of type image/png, image/jpeg, image/bmp, image/gif, image/tiff, or image/x-icon") % path)


if __name__ == '__main__':
    Embedder().run()
