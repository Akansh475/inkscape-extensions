# coding=utf-8
#
# pylint: disable=invalid-name
#
"""
Depreicated simpletransform replacements with documentation
"""

from inkex.deprecated import deprecate
from inkex.transforms import Transform, BoundingBox, cubic_extrema
from inkex.paths import Path

import inkex, cubicsuperpath

@deprecate
def parseTransform(transf, mat=None):
    """Transform(str).matrix"""
    if mat is not None:
        return (Transform(mat) * Transform(transf)).matrix
    return Transform(transf).matrix

@deprecate
def formatTransform(mat):
    """str(Transform(mat))"""
    return str(Transform(mat))

@deprecate
def invertTransform(mat):
    """-Transform(mat)"""
    return (-Transform(mat)).matrix

@deprecate
def composeTransform(mat1, mat2):
    """Transform(M1) * Transform(M2)"""
    return (Transform(mat1) * Transform(mat2)).matrix

@deprecate
def composeParents(node, mat):
    """elem.composed_transform() or elem.transform * Transform(mat)"""
    return (node.transform * Transform(mat)).matrix

@deprecate
def applyTransformToNode(mat, node):
    """elem.transform *= Transform(mat)"""
    node.transform *= Transform(mat)

@deprecate
def applyTransformToPoint(mat, pt):
    """Transform(mat).apply_to_point(pt)"""
    pt2 = Transform(mat).apply_to_point(pt)
    # Apply in place as original method was modifying arrays in place.
    # but don't do this in your code! This is not good code design.
    pt[0] = pt2[0]
    pt[1] = pt2[1]
    return pt2

@deprecate
def applyTransformToPath(mat, path):
    """XXX No replacement coded yet, HELP!"""
    for comp in path:
        for ctl in comp:
            for pt in ctl:
                applyTransformToPoint(mat, pt)

@deprecate
def fuseTransform(node):
    """XXX No replacement coded yet, HELP!"""
    if node.get('d')==None:
        #FIXME: how do you raise errors?
        raise AssertionError('can not fuse "transform" of elements that have no "d" attribute')
    t = node.get("transform")
    if t == None:
        return
    m = parseTransform(t)
    d = node.get('d')
    p = cubicsuperpath.parsePath(d)
    applyTransformToPath(m,p)
    node.set('d', cubicsuperpath.formatPath(p))
    del node.attrib["transform"]

@deprecate
def boxunion(b1, b2):
    """list(BoundingBox(b1) + BoundingBox(b2))"""
    return list(BoundingBox(b1) + BoundingBox(b2))

@deprecate
def roughBBox(path):
    """list(Path(path)).bounding_box())"""
    return list(Path(path).bounding_box())

@deprecate
def refinedBBox(path):
    """list(Path(path)).bounding_box())"""
    return list(Path(path).bounding_box())

@deprecate
def cubicExtrema(y0, y1, y2, y3):
    """from inkex.transforms import cubic_extrema"""
    return cubic_extrema(y0, y1, y2, y3)

@deprecate
def computeBBox(aList, mat=[[1,0,0],[0,1,0]]):
    """sum([node.bounding_box() for node in aList])"""
    return sum([node.bounding_box() for node in aList])

@deprecate
def computePointInNode(pt, node, mat=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]):
    """XXX No replacement coded yet, HELP!"""
    if node.getparent() is not None:
        applyTransformToPoint(invertTransform(composeParents(node, mat)), pt)
    return pt

