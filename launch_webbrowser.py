#!/usr/bin/env python
# coding=utf-8
# standard library
import webbrowser
import threading
from argparse import ArgumentParser
# local library
import inkex
from inkex.localization import _

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


