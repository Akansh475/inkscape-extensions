#!/usr/bin/env python
# standard library
import webbrowser
import threading
from argparse import ArgumentParser
# local library
import inkex
from inkex.localize import _

class VisitWebSiteWithoutLockingInkscape(threading.Thread):
    def __init__(self):
        threading.Thread.__init__ (self)
        parser = ArgumentParser()
        parser.add_argument("-u", "--url",
                          default="https://www.inkscape.org/",
                          help="The URL to open in web browser")
        self.options = parser.parse_args()

    def run(self):
        webbrowser.open(_(self.options.url))

if __name__ == '__main__':
    vwswli = VisitWebSiteWithoutLockingInkscape()
    vwswli.start()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
