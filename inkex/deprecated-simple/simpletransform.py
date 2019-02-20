# COPYRIGHT
#
# pylint: disable=invalid-name
#
"""
Depreicated simpletransform replacements with documentation
"""
  
from inkex.deprecated import deprecate
from inkex.transforms import Transform

import inkex, cubicsuperpath, bezmisc, simplestyle
import copy, math, re


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
                applyTransformToPoint(mat,pt)

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

####################################################################
##-- Some functions to compute a rough bbox of a given list of objects.
##-- this should be shipped out in an separate file...

@deprecate
def boxunion(b1,b2):
    """XXX No replacement coded yet, HELP!"""
    if b1 is None:
        return b2
    elif b2 is None:
        return b1    
    else:
        return((min(b1[0],b2[0]), max(b1[1],b2[1]), min(b1[2],b2[2]), max(b1[3],b2[3])))

@deprecate
def roughBBox(path):
    """XXX No replacement coded yet, HELP!"""
    xmin,xMax,ymin,yMax = path[0][0][0][0],path[0][0][0][0],path[0][0][0][1],path[0][0][0][1]
    for pathcomp in path:
        for ctl in pathcomp:
            for pt in ctl:
                xmin = min(xmin,pt[0])
                xMax = max(xMax,pt[0])
                ymin = min(ymin,pt[1])
                yMax = max(yMax,pt[1])
    return xmin,xMax,ymin,yMax

@deprecate
def refinedBBox(path):
    """XXX No replacement coded yet, HELP!"""
    xmin,xMax,ymin,yMax = path[0][0][1][0],path[0][0][1][0],path[0][0][1][1],path[0][0][1][1]
    for pathcomp in path:
        for i in range(1, len(pathcomp)):
            cmin, cmax = cubicExtrema(pathcomp[i-1][1][0], pathcomp[i-1][2][0], pathcomp[i][0][0], pathcomp[i][1][0])
            xmin = min(xmin, cmin)
            xMax = max(xMax, cmax)
            cmin, cmax = cubicExtrema(pathcomp[i-1][1][1], pathcomp[i-1][2][1], pathcomp[i][0][1], pathcomp[i][1][1])
            ymin = min(ymin, cmin)
            yMax = max(yMax, cmax)
    return xmin,xMax,ymin,yMax

@deprecate
def cubicExtrema(y0, y1, y2, y3):
    """Import from inkex.transforms instead"""
    from inkex.transforms import cubicExtrema
    return cubicExtrema(y0, y1, y2, y3)

@deprecate
def computeBBox(aList,mat=[[1,0,0],[0,1,0]]):
    """XXX No replacement coded yet, HELP!"""
    bbox=None
    for node in aList:
        m = parseTransform(node.get('transform'))
        m = composeTransform(mat,m)
        #TODO: text not supported!
        d = None
        if node.get("d"):
            d = node.get('d')
        elif node.get('points'):
            d = 'M' + node.get('points')
        elif node.tag in [ inkex.addNS('rect','svg'), 'rect', inkex.addNS('image','svg'), 'image' ]:
            d = 'M' + node.get('x', '0') + ',' + node.get('y', '0') + \
                'h' + node.get('width') + 'v' + node.get('height') + \
                'h-' + node.get('width')
        elif node.tag in [ inkex.addNS('line','svg'), 'line' ]:
            d = 'M' + node.get('x1') + ',' + node.get('y1') + \
                ' ' + node.get('x2') + ',' + node.get('y2')
        elif node.tag in [ inkex.addNS('circle','svg'), 'circle', \
                            inkex.addNS('ellipse','svg'), 'ellipse' ]:
            rx = node.get('r')
            if rx is not None:
                ry = rx
            else:
                rx = node.get('rx')
                ry = node.get('ry')
            cx = float(node.get('cx', '0'))
            cy = float(node.get('cy', '0'))
            x1 = cx - float(rx)
            x2 = cx + float(rx)
            d = 'M %f %f ' % (x1, cy) + \
                'A' + rx + ',' + ry + ' 0 1 0 %f,%f' % (x2, cy) + \
                'A' + rx + ',' + ry + ' 0 1 0 %f,%f' % (x1, cy)
 
        if d is not None:
            p = cubicsuperpath.parsePath(d)
            applyTransformToPath(m,p)
            bbox=boxunion(refinedBBox(p),bbox)

        elif node.tag == inkex.addNS('use','svg') or node.tag=='use':
            refid=node.get(inkex.addNS('href','xlink'))
            path = '//*[@id="%s"]' % refid[1:]
            refnode = node.xpath(path)
            bbox=boxunion(computeBBox(refnode,m),bbox)
            
        bbox=boxunion(computeBBox(node,m),bbox)
    return bbox

@deprecate
def computePointInNode(pt, node, mat=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]):
    """XXX No replacement coded yet, HELP!"""
    if node.getparent() is not None:
        applyTransformToPoint(invertTransform(composeParents(node, mat)), pt)
    return pt

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
