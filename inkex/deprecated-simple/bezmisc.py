# COPYRIGHT
"""DOCSTRING"""

import math, cmath

def rootWrapper(a,b,c,d):
    """Unknown"""

def bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3))):
    """parametric bezier"""

def linebezierintersect(((lx1,ly1),(lx2,ly2)),((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3))):
    """parametric line"""

def bezierpointatt(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)),t):
    """something"""

def bezierslopeatt(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)),t):
    """something"""

def beziertatslope(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)),(dy,dx)):
    """Unknown"""

def tpoint((x1,y1),(x2,y2),t):
    """Unknown"""

def beziersplitatt(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)),t):
    """Unknown"""

def pointdistance((x1,y1),(x2,y2)):
    """Uknown"""

def Gravesen_addifclose(b, len, error = 0.001):
    """Unknown"""

def bezierlengthGravesen(b, error = 0.001):
    """Unknown"""

def balf(t):
    """Unknown"""
    retval = (balfax*(t**2) + balfbx*t + balfcx)**2 + (balfay*(t**2) + balfby*t + balfcy)**2
    return math.sqrt(retval)

def Simpson(f, a, b, n_limit, tolerance):
    """Unknown"""

def bezierlengthSimpson(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)), tolerance = 0.001):
    """Unknown"""

def beziertatlength(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)), l = 0.5, tolerance = 0.001):
    """Unknown"""

#default bezier length method
bezierlength = bezierlengthSimpson
