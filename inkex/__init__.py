# coding=utf-8
"""
This describes the core API for the inkex core modules.

They provide the basis from which you can develop your inkscape extension.
"""

# pylint: disable=wildcard-import
from __future__ import print_function

from .generic import *
from .utils import *
from .styles import *
from .paths import *
from .colors import *
from .transforms import *

# legacy proxies
from .deprecated import Effect
from .deprecated import optparse
from .deprecated import InkOption
from .deprecated import etree
from .deprecated import localize

# legacy functions
from .deprecated import unittouu
