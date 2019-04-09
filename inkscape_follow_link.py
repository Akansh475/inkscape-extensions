#!/usr/bin/env python
# coding=utf-8

import threading
import webbrowser

import inkex
from inkex.elements import Anchor
from inkex.generic import EffectExtension

class VisitWebSiteWithoutLockingInkscape(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__ (self)
        self.url = url

    def run(self):
        webbrowser.open(self.url)

class FollowLink(EffectExtension):
    def effect(self):
        if self.options.ids:
            for node in self.svg.selected.values():
                if isinstance(node, Anchor):
                    self.url = node.get(inkex.addNS('href','xlink'))
                    vwswli = VisitWebSiteWithoutLockingInkscape(self.url)
                    vwswli.start()
                    #inkex.errormsg("Link: %s" % self.url)
                    break


if __name__ == '__main__':
    FollowLink().run()

