#!/usr/bin/env python
# coding=utf-8

import webbrowser
import threading
from argparse import ArgumentParser

class ThreadWebsite(threading.Thread):
    """Visit website without locking Inkscape"""
    def __init__(self):
        threading.Thread.__init__(self)
        parser = ArgumentParser()
        parser.add_argument("-u", "--url",
                            default="https://www.inkscape.org/",
                            help="The URL to open in web browser")
        self.options = parser.parse_args()

    def run(self):
        webbrowser.open(_(self.options.url))

if __name__ == '__main__':
    ThreadWebsite().start()
