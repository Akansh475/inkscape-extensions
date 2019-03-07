#!/usr/bin/env python
# coding=utf-8

# Written by Jabiertxof
# V.06

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from lxml import etree

from inkex.base import InkscapeExtension, SvgThroughMixin
from inkex.utils import NSS, addNS


class C(SvgThroughMixin, InkscapeExtension):
    def __init__(self):
        super(C, self).__init__()
        self.arg_parser.add_argument("-w", "--width",
                                     action="store", type=int,
                                     dest="desktop_width", default=100, help="Custom width")
        self.arg_parser.add_argument("-z", "--height",
                                     action="store", type=int,
                                     dest="desktop_height", default=100, help="Custom height")

    def effect(self):
        saveout = sys.stdout
        sys.stdout = sys.stderr
        try:
            self._effect_stderr()
        finally:
            sys.stdout = saveout

    def _effect_stderr(self):
        width = self.options.desktop_width
        height = self.options.desktop_height
        if height == 0 or width == 0:
            return
        factor = width / height
        path = os.path.dirname(os.path.realpath(__file__))
        self.document = etree.parse(os.path.join(path, "seamless_pattern.svg"))
        root = self.document.getroot()
        root.set("id", "SVGRoot")
        root.set("width", str(width))
        root.set("height", str(height))
        root.set("viewBox", "0 0 {} {}".format(str(width), str(height)))

        xpath_str = '//svg:rect[@id="clipPathRect"]'
        clipPathRect = root.xpath(xpath_str, namespaces=NSS)
        if clipPathRect:
            clipPathRect[0].set("width", str(width))
            clipPathRect[0].set("height", str(height))

        xpath_str = '//svg:pattern[@id="Checkerboard"]'
        designZoneData = root.xpath(xpath_str, namespaces=NSS)
        if designZoneData:
            if factor <= 1:
                designZoneData[0].set("patternTransform", "scale({},{})".format(str(10), str(factor * 10)))
            else:
                designZoneData[0].set("patternTransform", "scale({},{})".format(str(10 / factor), str(10)))

        xpath_str = '//svg:g[@id="designTop"] | //svg:g[@id="designBottom"]'
        designZone = root.xpath(xpath_str, namespaces=NSS)
        if designZone:
            designZone[0].set("transform", "scale({},{})".format(str(width / 100), str(height / 100)))
            designZone[1].set("transform", "scale({},{})".format(str(width / 100), str(height / 100)))

        xpath_str = '//svg:g[@id="designTop"]/child::*'
        designZoneData = root.xpath(xpath_str, namespaces=NSS)
        if designZoneData:
            if factor <= 1:
                designZoneData[0].set("transform", "scale(1,{})".format(str(factor)))
                designZoneData[1].set("transform", "scale(1,{})".format(str(factor)))
                designZoneData[2].set("transform", "scale(1,{})".format(str(factor)))
            else:
                designZoneData[0].set("transform", "scale({},1)".format(str(1 / factor)))
                designZoneData[1].set("transform", "scale({},1)".format(str(1 / factor)))
                designZoneData[2].set("transform", "scale({},1)".format(str(1 / factor)))

        xpath_str = '//svg:g[@id="textPreview"]'
        textPreview = root.xpath(xpath_str, namespaces=NSS)
        if textPreview:
            if factor <= 1:
                textPreview[0].set("transform", "translate({},0) scale({},{})".format(str(width * 2),
                                                                                      str(width / 100),
                                                                                      str((height / 1000) * factor)))
            else:
                textPreview[0].set("transform", "translate({},0) scale({},{})".format(str(width * 2),
                                                                                      str((width / 100) / factor),
                                                                                      str(height / 1000)))

        xpath_str = '//svg:g[@id="infoGroup"]'
        infoGroup = root.xpath(xpath_str, namespaces=NSS)
        if infoGroup:
            if factor <= 1:
                infoGroup[0].set("transform", "scale({},{})".format(str(width / 100), str((height / 100) * factor)))
            else:
                infoGroup[0].set("transform", "scale({},{})".format(str(width / 1000), str((height / 1000) * factor)))

        xpath_str = '//svg:use[@id="top1"] | //svg:use[@id="bottom1"]'
        pattern1 = root.xpath(xpath_str, namespaces=NSS)
        if pattern1:
            pattern1[0].set("transform", "translate({},{})".format(str(-width), str(-height)))
            pattern1[1].set("transform", "translate({},{})".format(str(-width), str(-height)))

        xpath_str = '//svg:use[@id="top2"] | //svg:use[@id="bottom2"]'
        pattern2 = root.xpath(xpath_str, namespaces=NSS)
        if pattern2:
            pattern2[0].set("transform", "translate(0,{})".format(str(-height)))
            pattern2[1].set("transform", "translate(0,{})".format(str(-height)))

        xpath_str = '//svg:use[@id="top3"] | //svg:use[@id="bottom3"]'
        pattern3 = root.xpath(xpath_str, namespaces=NSS)
        if pattern3:
            pattern3[0].set("transform", "translate({},{})".format(str(width), str(-height)))
            pattern3[1].set("transform", "translate({},{})".format(str(width), str(-height)))

        xpath_str = '//svg:use[@id="top4"] | //svg:use[@id="bottom4"]'
        pattern4 = root.xpath(xpath_str, namespaces=NSS)
        if pattern4:
            pattern4[0].set("transform", "translate({},0)".format(str(-width)))
            pattern4[1].set("transform", "translate({},0)".format(str(-width)))

        xpath_str = '//svg:use[@id="top5"] | //svg:use[@id="bottom5"]'
        pattern5 = root.xpath(xpath_str, namespaces=NSS)
        if pattern5:
            pattern5[0].set("transform", "translate(0,0)")
            pattern5[1].set("transform", "translate(0,0)")

        xpath_str = '//svg:use[@id="top6"] | //svg:use[@id="bottom6"]'
        pattern6 = root.xpath(xpath_str, namespaces=NSS)
        if pattern6:
            pattern6[0].set("transform", "translate({},0)".format(str(width)))
            pattern6[1].set("transform", "translate({},0)".format(str(width)))

        xpath_str = '//svg:use[@id="top7"] | //svg:use[@id="bottom7"]'
        pattern7 = root.xpath(xpath_str, namespaces=NSS)
        if pattern7:
            pattern7[0].set("transform", "translate({},{})".format(str(-width), str(height)))
            pattern7[1].set("transform", "translate({},{})".format(str(-width), str(height)))

        xpath_str = '//svg:use[@id="top8"] | //svg:use[@id="bottom8"]'
        pattern8 = root.xpath(xpath_str, namespaces=NSS)
        if pattern8:
            pattern8[0].set("transform", "translate(0,{})".format(str(height)))
            pattern8[1].set("transform", "translate(0,{})".format(str(height)))

        xpath_str = '//svg:use[@id="top9"] | //svg:use[@id="bottom9"]'
        pattern9 = root.xpath(xpath_str, namespaces=NSS)
        if pattern9:
            pattern9[0].set("transform", "translate({},{})".format(str(width), str(height)))
            pattern9[1].set("transform", "translate({},{})".format(str(width), str(height)))

        xpath_str = '//svg:use[@id="clonePreview1"]'
        clonePreview1 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview1:
            clonePreview1[0].set("transform", "translate(0,{})".format(str(height)))

        xpath_str = '//svg:use[@id="clonePreview2"]'
        clonePreview2 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview2:
            clonePreview2[0].set("transform", "translate(0,{})".format(str(height * 2)))

        xpath_str = '//svg:use[@id="clonePreview3"]'
        clonePreview3 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview3:
            clonePreview3[0].set("transform", "translate({},0)".format(str(width)))

        xpath_str = '//svg:use[@id="clonePreview4"]'
        clonePreview4 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview4:
            clonePreview4[0].set("transform", "translate({},{})".format(str(width), str(height)))

        xpath_str = '//svg:use[@id="clonePreview5"]'
        clonePreview5 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview5:
            clonePreview5[0].set("transform", "translate({},{})".format(str(width), str(height * 2)))

        xpath_str = '//svg:use[@id="clonePreview6"]'
        clonePreview6 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview6:
            clonePreview6[0].set("transform", "translate({}, 0)".format(str(width * 2)))

        xpath_str = '//svg:use[@id="clonePreview7"]'
        clonePreview7 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview7:
            clonePreview7[0].set("transform", "translate({},{})".format(str(width * 2), str(height)))

        xpath_str = '//svg:use[@id="clonePreview8"]'
        clonePreview8 = root.xpath(xpath_str, namespaces=NSS)
        if clonePreview8:
            clonePreview8[0].set("transform", "translate({},{})".format(str(width * 2), str(height * 2)))

        xpath_str = '//svg:use[@id="fullPatternClone"]'
        patternGenerator = root.xpath(xpath_str, namespaces=NSS)
        if patternGenerator:
            patternGenerator[0].set("transform", "translate({},-{})".format(str(width * 2), str(height)))
            patternGenerator[0].set("{http://www.inkscape.org/namespaces/inkscape}tile-cx", str(width / 2))
            patternGenerator[0].set("{http://www.inkscape.org/namespaces/inkscape}tile-cy", str(height / 2))
            patternGenerator[0].set("{http://www.inkscape.org/namespaces/inkscape}tile-w", str(width))
            patternGenerator[0].set("{http://www.inkscape.org/namespaces/inkscape}tile-h", str(height))
            patternGenerator[0].set("{http://www.inkscape.org/namespaces/inkscape}tile-x0", str(width))
            patternGenerator[0].set("{http://www.inkscape.org/namespaces/inkscape}tile-y0", str(height))
            patternGenerator[0].set("width", str(width))
            patternGenerator[0].set("height", str(height))

        namedview = root.find(addNS('namedview', 'sodipodi'))
        if namedview is None:
            namedview = etree.SubElement(root, addNS('namedview', 'sodipodi'))

        namedview.set(addNS('document-units', 'inkscape'), 'px')

        namedview.set(addNS('cx', 'inkscape'), str((width * 5.5) / 2))
        namedview.set(addNS('cy', 'inkscape'), "0")
        namedview.set(addNS('zoom', 'inkscape'), str(1/ (width / 100)))


if __name__ == '__main__':
    C().run()
