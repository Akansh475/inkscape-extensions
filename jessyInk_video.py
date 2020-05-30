#!/usr/bin/env python
#
# Copyright 2008, 2009 Hannes Hochreiner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import re
from copy import deepcopy

import inkex
from inkex.localization import inkex_gettext as _
from inkex.utils import NSS
NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

class Video(inkex.EffectExtension):
    """Add jessyink video"""
    def add_arguments(self, pars):
        self.arg_parser.add_argument('--tab', dest='what')

    def effect(self):
        # Check version.
        scripts = self.svg.getElement("//svg:script[@jessyink:version='1.5.5']")
        if scripts is None:
            raise inkex.AbortExtension(_(
                "The JessyInk script is not installed in this SVG file or has a "
                "different version than the JessyInk extensions. Please select "
                "\"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" "
                "menu to install or update the JessyInk script.\n\n"))

        base_view = self.svg.xpath("//sodipodi:namedview[@id='base']")
        if base_view is None:
            raise inkex.AbortExtension(_(
                "Could not obtain the selected layer for inclusion of the video element."))

        layer = self.svg.get_current_layer()
        if layer is None:
            raise inkex.AbortExtension(_(
                "Could not obtain the selected layer for inclusion of the video element.\n\n"))

        template = inkex.load_svg(self.get_resource('jessyInk_video.svg'))
        root = template.getroot()

        elem = root.getElement("//svg:g[@jessyink:element='core.video']").copy()
        node_dict = findInternalLinks(elem, root)
        deleteIds(elem)

        ids = {}

        for key in node_dict:
            ids[key] = getNewId("jessyink.core.video", self.document)
            deleteIds(node_dict[key])
            node_dict[key].attrib['id'] = ids[key]
            elem.insert(0, node_dict[key])

        for nd_iter in elem.iter():
            for attrs in nd_iter.attrib:
                for entires in ids:
                    nd_iter.attrib[attrs] = nd_iter.attrib[attrs].replace("#" + entires, "#" + ids[entires])

        # Append element.
        layer.append(elem)

def findInternalLinks(node, docRoot, node_dict = {}):
    for entry in re.findall(br"url\(#.*\)", node.tostring()):
        entry = entry.decode()
        linkId = entry[5:len(entry) - 1]

        if linkId not in node_dict:
            node_dict[linkId] = deepcopy(docRoot.xpath("//*[@id='" + linkId + "']", namespaces=NSS)[0])
            node_dict = findInternalLinks(node_dict[linkId], docRoot, node_dict)

    for entry in node.iter():
        if '{' + NSS['xlink'] + '}href' in entry.attrib:
            linkId = entry.attrib['{' + NSS['xlink'] + '}href'][1:len(entry.attrib['{' + NSS['xlink'] + '}href'])]

            if linkId not in node_dict:
                node_dict[linkId] = deepcopy(docRoot.xpath("//*[@id='" + linkId + "']", namespaces=NSS)[0])
                node_dict = findInternalLinks(node_dict[linkId], docRoot, node_dict)

    return node_dict

def getNewId(prefix, docRoot):
    import datetime

    number = datetime.datetime.now().microsecond

    while len(docRoot.xpath("//*[@id='" + prefix + str(number) + "']", namespaces=NSS)) > 0:
        number += 1

    return prefix + str(number)

def deleteIds(node):
    for entry in node.iter():
        if 'id' in entry.attrib:
            del entry.attrib['id']

if __name__ == '__main__':
    Video().run()
