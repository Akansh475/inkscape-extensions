#!/usr/bin/env python
# coding=utf-8

# Written by Tavmjong Bah

import re
import inkex

class EmptyVideo(inkex.Effect):
    """Empty video template"""
    def __init__(self):
        super(EmptyVideo, self).__init__()
        self.arg_parser.add_argument("-s", "--size", type=str, dest="video_size",
                                     default="16", help="Video size")
        self.arg_parser.add_argument("-w", "--width", type=int, dest="video_width",
                                     default="1920", help="Custom width")
        self.arg_parser.add_argument("-z", "--height", type=int, dest="video_height",
                                     default="1080", help="Custom height")

    def effect(self):
        size = self.options.video_size
        width = self.options.video_width
        height = self.options.video_height

        if size != "Custom":
            p = re.compile('([0-9]*)x([0-9]*)')
            m = p.match( size )
            if m is None:
                return inkex.errormsg("Size must be specified!")
            width = int(m.group(1))
            height = int(m.group(2))

        root = self.document.getroot()
        root.set("id", "SVGRoot")
        root.set("width", str(width) + 'px')
        root.set("height", str(height) + 'px')
        root.set("viewBox", "0 0 " + str(width) + " " + str(height))

        namedview = root.find(inkex.addNS('namedview', 'sodipodi'))
        if namedview is None:
            namedview = inkex.etree.SubElement( root, inkex.addNS('namedview', 'sodipodi'))

        namedview.set(inkex.addNS('document-units', 'inkscape'), 'px')
        namedview.set(inkex.addNS('cx', 'inkscape'), str(width/2.0))
        namedview.set(inkex.addNS('cy', 'inkscape'), str(height/2.0))

if __name__ == '__main__':
    EmptyVideo().run()
