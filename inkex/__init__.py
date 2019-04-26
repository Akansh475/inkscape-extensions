# coding=utf-8
from __future__ import print_function

from .generic import (
    Effect, EffectExtension, OutputExtension, InputExtension, GenerateExtension
)
from .utils import *
from .bezier import *
from .styles import *
from .paths import *
from .colors import *
from .tween import *
from .transforms import *
from .cubic_paths import *

# legacy proxies
from .deprecated import optparse
from .deprecated import InkOption
from .deprecated import etree
