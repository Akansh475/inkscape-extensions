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

import os
import re
from copy import deepcopy

from lxml import etree

import inkex
from inkex.localization import inkex_gettext as _
from inkex.utils import NSS
NSS[u"jessyink"] = u"https://launchpad.net/jessyink"

class Video(inkex.EffectExtension):
    def add_arguments(self, pars):
        self.arg_parser.add_argument('--tab', dest='what')

    def effect(self):
        # Check version.
        scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.5']", namespaces=NSS)

        if len(scriptNodes) != 1:
            inkex.errormsg(_("The JessyInk script is not installed in this SVG file or has a different version than the JessyInk extensions. Please select \"install/update...\" from the \"JessyInk\" sub-menu of the \"Extensions\" menu to install or update the JessyInk script.\n\n"))

        baseView = self.document.xpath("//sodipodi:namedview[@id='base']", namespaces=NSS)

        if len(baseView) != 1:
            inkex.errormsg(_("Could not obtain the selected layer for inclusion of the video element.\n\n"))

        layer = self.document.xpath("//svg:g[@id='" + baseView[0].attrib["{" + NSS["inkscape"] + "}current-layer"] + "']", namespaces=NSS)

        if len(layer) != 1:
            inkex.errormsg(_("Could not obtain the selected layer for inclusion of the video element.\n\n"))

        # Parse template file.
        tmplFile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jessyInk_video.svg'), 'rb')
        tmplRoot = etree.fromstring(tmplFile.read())
        tmplFile.close()

        elem = deepcopy(tmplRoot.xpath("//svg:g[@jessyink:element='core.video']", namespaces=NSS)[0])
        nodeDict = findInternalLinks(elem, tmplRoot)

        deleteIds(elem)

        idSubst = {}

        for key in nodeDict:
            idSubst[key] = getNewId("jessyink.core.video", self.document)
            deleteIds(nodeDict[key])
            nodeDict[key].attrib['id'] = idSubst[key]
            elem.insert(0, nodeDict[key])

        for ndIter in elem.iter():
            for attrIter in ndIter.attrib:
                for entryIter in idSubst:
                    ndIter.attrib[attrIter] = ndIter.attrib[attrIter].replace("#" + entryIter, "#" + idSubst[entryIter])

        # Append element.
        layer[0].append(elem)

def findInternalLinks(node, docRoot, nodeDict = {}):
    for entry in re.findall(br"url\(#.*\)", etree.tostring(node)):
        entry = entry.decode()
        linkId = entry[5:len(entry) - 1]

        if linkId not in nodeDict:
            nodeDict[linkId] = deepcopy(docRoot.xpath("//*[@id='" + linkId + "']", namespaces=NSS)[0])
            nodeDict = findInternalLinks(nodeDict[linkId], docRoot, nodeDict)

    for entry in node.iter():
        if '{' + NSS['xlink'] + '}href' in entry.attrib:
            linkId = entry.attrib['{' + NSS['xlink'] + '}href'][1:len(entry.attrib['{' + NSS['xlink'] + '}href'])]

            if linkId not in nodeDict:
                nodeDict[linkId] = deepcopy(docRoot.xpath("//*[@id='" + linkId + "']", namespaces=NSS)[0])
                nodeDict = findInternalLinks(nodeDict[linkId], docRoot, nodeDict)

    return nodeDict

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
