# COPYRIGHT
#
# pylint: disable=invalid-name
#
"""
Depreicated simplepath replacements with documentation
"""

from inkex.deprecated import deprecate
from inkex.paths import Path

@deprecate
def parsePath(d):
    """element.path.to_arrays()"""
    return Path(d).to_arrays()

@deprecate
def formatPath(a):
    """str(element.path) or str(Path(array))"""
    return str(Path(a))

@deprecate
def translatePath(p, x, y):
    """Path(array).translate(x, y)"""
    return (Path(p) + (x, y)).to_arrays()

@deprecate
def scalePath(p, x, y):
    """Path(array).scale(x, y)"""
    return (Path(p) * (x, y)).to_arrays()

@deprecate
def rotatePath(p, a, cx=0, cy=0):
    """Path(array).rotate(angle_degrees, center_x, center_y)"""
    path = Path(p)
    path.rotate(a, cx, cy)
    return path.to_arrays()

