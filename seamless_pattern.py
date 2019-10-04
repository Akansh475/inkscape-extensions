#!/usr/bin/env python
# coding=utf-8

# Written by Jabiertxof
# V.06

from __future__ import absolute_import, division, print_function, unicode_literals

import os

import inkex
from inkex.elements import load_svg

class SeamlessPattern(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("-w", "--width", type=int, default=100,
                          dest="desktop_width", help="Custom width")
        pars.add_argument("-z", "--height", type=int, default=100,
                          dest="desktop_height", help="Custom height")

    def get_template(self, name):
        path = os.path.dirname(os.path.realpath(__file__))
        return load_svg(os.path.join(path, name))

    def effect(self):
        width = self.options.desktop_width
        height = self.options.desktop_height
        if height == 0 or width == 0:
            return
        factor = width / height

        self.document = self.get_template("seamless_pattern.svg")
        root = self.document.getroot()
        root.set("id", "SVGRoot")
        root.set("width", str(width))
        root.set("height", str(height))
        root.set("viewBox", "0 0 {} {}".format(str(width), str(height)))

        xpath_str = '//svg:rect[@id="clipPathRect"]'
        clipPathRect = root.xpath(xpath_str)
        if clipPathRect:
            clipPathRect[0].set("width", str(width))
            clipPathRect[0].set("height", str(height))

        xpath_str = '//svg:pattern[@id="Checkerboard"]'
        designZoneData = root.xpath(xpath_str)
        if designZoneData:
            if factor <= 1:
                designZoneData[0].set("patternTransform", "scale({},{})".format(str(10), str(factor * 10)))
            else:
                designZoneData[0].set("patternTransform", "scale({},{})".format(str(10 / factor), str(10)))

        xpath_str = '//svg:g[@id="designTop"] | //svg:g[@id="designBottom"]'
        designZone = root.xpath(xpath_str)
        if designZone:
            designZone[0].set("transform", "scale({},{})".format(str(width / 100), str(height / 100)))
            designZone[1].set("transform", "scale({},{})".format(str(width / 100), str(height / 100)))

        xpath_str = '//svg:g[@id="designTop"]/child::*'
        designZoneData = root.xpath(xpath_str)
        if designZoneData:
            if factor <= 1:
                designZoneData[0].set("transform", "scale(1,{})".format(str(factor)))
                designZoneData[1].set("transform", "scale(1,{})".format(str(factor)))
                designZoneData[2].set("transform", "scale(1,{})".format(str(factor)))
            else:
                designZoneData[0].set("transform", "scale({},1)".format(str(1 / factor)))
                designZoneData[1].set("transform", "scale({},1)".format(str(1 / factor)))
                designZoneData[2].set("transform", "scale({},1)".format(str(1 / factor)))

        text_preview = root.getElementById('textPreview')
        if text_preview is not None:
            x = width / 100 / factor
            y = height / 1000
            if factor <= 1:
                x *= factor
                y *= factor
            text_preview.transform = inkex.Transform(translate=(width * 2, 0), scale=(x, y))

        info_group = root.getElementById('info_group')
        if info_group is not None:
            scale = 100 if factor <= 1 else 1000
            info_group.transform = inkex.Transform(scale=(width / scale, height / scale * factor))

        sides = [(x, y) for y in (-height, 0, height) for x in (-width, 0, width)]
        for i, (x, y) in enumerate(sides):
            top = root.getElementById('top{i}'.format(i=i+1))
            bottom = root.getElementById('bottom{i}'.format(i=i+1))
            if top is not None and bottom is not None:
                bottom.transform = top.transform = inkex.Transform(translate=(x, y))

        clones = [(x, y) for x in (0, width, width * 2) for y in (0, height, height * 2)]
        for i, (x, y) in enumerate(clones):
            preview = root.getElementById("clonePreview{i}".format(i=i))
            if preview is not None:
                preview.transform = inkex.Transform(translate=(x, y))

        pattern_generator = root.getElementById('fullPatternClone')
        if pattern_generator is not None:
            pattern_generator.transform = inkex.Transform(translate=(width * 2, -height))
            pattern_generator.set("inkscape:tile-cx", width / 2)
            pattern_generator.set("inkscape:tile-cy", height / 2)
            pattern_generator.set("inkscape:tile-w", width)
            pattern_generator.set("inkscape:tile-h", height)
            pattern_generator.set("inkscape:tile-x0", width)
            pattern_generator.set("inkscape:tile-y0", height)
            pattern_generator.set("width", width)
            pattern_generator.set("height", height)

        namedview = root.namedview
        namedview.set('inkscape:document-units', 'px')
        namedview.set('inkscape:cx', (width * 5.5) / 2)
        namedview.set('inkscape:cy', "0")
        namedview.set('inkscape:zoom', 1 / (width / 100))

if __name__ == '__main__':
    SeamlessPattern().run()
