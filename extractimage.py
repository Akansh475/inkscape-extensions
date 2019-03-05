#!/usr/bin/env python 
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
"""
Extract emebeded images.
"""

import os
import base64

import inkex
from inkex import inkbool


class ExtractImage(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--desc")
        self.arg_parser.add_argument("-s", "--selectedonly",
            action="store", type=inkbool,
            dest="selectedonly", default=True,
            help="extract only selected images")
        self.arg_parser.add_argument("--filepath",
                        action="store", type=str,
                        dest="filepath", default=None,
                        help="")
    def effect(self):
        # if slectedonly is enabled and there is a selection only extractselected
        # images. otherwise extract all images
        if (self.options.selectedonly):
            self.extractSelected(self.document, self.svg.selected)
        else:
            self.extractAll(self.document)

    def extractSelected(self, document, selected):
        self.document=document
        self.svg.selected=selected
        if (self.options.ids):
            for id, node in selected.items():
                if node.tag == inkex.addNS('image','svg'):
                    self.extract_image(node)

    def extractAll(self, document):
        self.document=document #not that nice... oh well
        path = '//svg:image'
        for node in self.document.getroot().xpath(path, namespaces=inkex.NSS):
            self.extract_image(node)

    def mime_to_ext(self, mime):
        part = mime.split('/', 1)[1].split('+')[0]
        return {
            'png'     : '.png',
            'svg+xml' : '.svg',
            'bmp'     : '.bmp',
            'jpeg'    : '.jpg',
            'jpg'     : '.jpg', #bogus mime
            'icon'    : '.ico',
            'gif'     : '.gif',
            'wmf'     : '.wmf',
            'emf'     : '.emf',
        }.get(part, part)


    def extract_image(self, node):
        """
        Extract the node as if it were an image.
        """

        # exbed the first embedded image
        path = self.options.filepath
        if path == '':
            return # No filepath provided (error?)

        if node.tag != inkex.addNS('image', 'svg'):
            inkex.errormsg("Not an image element")
            return # Not an image tag

        xlink = node.get(inkex.addNS('href', 'xlink'))
        if not xlink.startswith('data:'):
            inkex.errormsg("Not an image element")
            return # Not embeded data

        data = xlink[5:]
        if ',' not in data or ';' not in data:
            inkex.errormsg("Invalid image format found")
            return

        (mimetype, data) = data.split(';', 1)
        (base, data) = data.split(',', 1)

        if base != 'base64':
            inkex.errormsg("Can't decode encoding: {}".format(base))

        file_ext = self.mime_to_ext(mimetype)

        pathwext = path + file_ext
        if os.path.isfile(pathwext):
            pathwext = path + "_" + node.get("id") + file_ext

        if not os.path.isabs(pathwext):
            if os.name == 'nt':
                pathwext = os.path.join(os.environ['USERPROFILE'], pathwext)
            else:
                pathwext = os.path.join(os.path.expanduser("~"), pathwext)

        inkex.errormsg('Image extracted to: %s' % pathwext)

        with open(pathwext, 'wb') as fhl:
            fhl.write(base64.decodestring(data))

        # absolute for making in-mem cycles work
        node.set(inkex.addNS('href', 'xlink'), os.path.realpath(pathwext))

if __name__ == '__main__':
    ExtractImage().run()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
