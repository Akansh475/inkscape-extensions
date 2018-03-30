#!/usr/bin/env python
#
# Copyright (C) 2010 Nick Drobchenko, nick@cnc-club.ru
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Basic common utility functions for calculated things
"""

import sys
import math
import cmath

from itertools import tee
from .const import X, Y, NSS, PY3
from .bezier import beziertatlength, bezierlength

def debug(what):
    """Print debug message if debugging is switched on"""
    sys.stderr.write(str(what) + "\n")
    return what

def errormsg(msg):
    """Intended for end-user-visible error messages.

       (Currently just writes to stderr with an appended newline, but could do
       something better in future: e.g. could add markup to distinguish error
       messages from status messages or debugging output.)

       Note that this should always be combined with translation:

         import inkex
         ...
         inkex.errormsg(_("This extension requires two selected paths."))
    """
    if PY3:
        sys.stderr.write(msg)
    elif isinstance(msg, unicode):
        sys.stderr.write(msg.encode("utf-8") + "\n")
    else:
        sys.stderr.write((unicode(msg, "utf-8", errors='replace') + "\n").encode("utf-8"))

def to(kind): # pylint: disable=invalid-name
    """
    Decorator which will turn a generator into a list, tuple or other object type.
    """
    def _inner(call):
        def _outer(*args, **kw):
            return kind(call(*args, **kw))
        return _outer
    return _inner

def addNS(tag, ns=None): # pylint: disable=invalid-name
    """Add a known namespace to a name for use with lxml"""
    val = tag
    if ns is not None and len(ns) > 0 and ns in NSS and len(tag) > 0 and tag[0] != '{':
        val = "{%s}%s" % (NSS[ns], tag)
    return val

def pairwise(iterable):
    "Iterate over a list with overlapping pairs (see itertools recipies)"
    first, then = tee(iterable)
    next(then, None)
    return zip(first, then)

def are_near_relative(point_a, point_b, eps):
    """Return true if the points are near to eps"""
    return (point_a - point_b <= point_a * eps) and (point_a - point_b >= -point_a * eps)

def numsegs(csp):
    """Returns the number of segments in the path"""
    return sum([len(p)-1 for p in csp])

def bezlenapprx(sp1, sp2):
    return pointdistance(sp1[1], sp1[2])\
         + pointdistance(sp1[2], sp2[0])\
         + pointdistance(sp2[0], sp2[1])

def tpoint(point_a, point_b, time=0.5):
    return point_a[X] + time * (point_b[X] - point_a[X]),\
           point_a[Y] + time * (point_b[Y] - point_a[Y])

def pointdistance(point_a, point_b):
    """The size of the line between two points"""
    return math.sqrt(((point_b[X] - point_a[X]) ** 2) + ((point_b[Y] - point_a[Y]) ** 2))

def interpcoord(coord_a, coord_b, time):
    """Interpolate single coordinate by the amount of time"""
    return coord_a + ((coord_b - coord_a) * time)

def interppoints(point1, point2, time):
    """Interpolate coordinate points by amount of time"""
    return [interpcoord(point1[X], point2[X], time), interpcoord(point1[Y], point2[Y], time)]

def cspbezsplit(sp1, sp2, time=0.5):
    m1 = tpoint(sp1[1], sp1[2], time)
    m2 = tpoint(sp1[2], sp2[0], time)
    m3 = tpoint(sp2[0], sp2[1], time)
    m4 = tpoint(m1, m2, time)
    m5 = tpoint(m2, m3, time)
    m = tpoint(m4, m5, time)
    return [[sp1[0][:],sp1[1][:],m1], [m4,m,m5], [m3,sp2[1][:],sp2[2][:]]]

def cspbezsplitatlength(sp1, sp2, l=0.5, tolerance=0.001):
    bez = (sp1[1][:],sp1[2][:],sp2[0][:],sp2[1][:])
    time = beziertatlength(bez, l, tolerance)
    return cspbezsplit(sp1, sp2, time)

def cspseglength(sp1,sp2, tolerance=0.001):
    bez = (sp1[1][:], sp1[2][:], sp2[0][:], sp2[1][:])
    return bezierlength(bez, tolerance)

def csplength(csp):
    total = 0 
    lengths = []
    for sp in csp:
        lengths.append([])
        for i in xrange(1,len(sp)):
            l = cspseglength(sp[i-1],sp[i])
            lengths[-1].append(l)
            total += l
    return lengths, total

def csparea(csp):
    area = 0.0 
    for sp in csp:
        if len(sp) < 2: continue
        for i in range(len(sp)):            # calculate polygon area
            area += 0.5*sp[i-1][1][0]*(sp[i][1][1] - sp[i-2][1][1])
        for i in range(1, len(sp)):         # add contribution from cubic Bezier 
            vec_x = numpy.matrix([sp[i-1][1][0], sp[i-1][2][0], sp[i][0][0], sp[i][1][0]])
            vec_y = numpy.matrix([sp[i-1][1][1], sp[i-1][2][1], sp[i][0][1], sp[i][1][1]])
            area += 0.15*(vec_x*mat_area*vec_y.T)[0,0]
    return -area

def cspcofm(csp):
    area = csparea(csp)
    xc = 0.0 
    yc = 0.0 
    if abs(area) < 1.e-8:
        inkex.errormsg(_("Area is zero, cannot calculate Center of Mass"))
        return 0, 0
    for sp in csp:
        for i in range(len(sp)):            # calculate polygon moment
            xc += sp[i-1][1][1]*(sp[i-2][1][0] - sp[i][1][0])*(sp[i-2][1][0] + sp[i-1][1][0] + sp[i][1][0])/6
            yc += sp[i-1][1][0]*(sp[i][1][1] - sp[i-2][1][1])*(sp[i-2][1][1] + sp[i-1][1][1] + sp[i][1][1])/6
        for i in range(1, len(sp)):         # add contribution from cubic Bezier
            vec_x = numpy.matrix([sp[i-1][1][0], sp[i-1][2][0], sp[i][0][0], sp[i][1][0]])
            vec_y = numpy.matrix([sp[i-1][1][1], sp[i-1][2][1], sp[i][0][1], sp[i][1][1]])
            vec_t = numpy.matrix([(vec_x*mat_cofm_0*vec_y.T)[0,0], (vec_x*mat_cofm_1*vec_y.T)[0,0], (vec_x*mat_cofm_2*vec_y.T)[0,0], (vec_x*mat_cofm_3*vec_y.T)[0,0]])
            xc += (vec_x*vec_t.T)[0,0]/280
            yc += (vec_y*vec_t.T)[0,0]/280
    return -xc/area, -yc/area

def bezierparameterize(arg):
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = arg
    #parametric bezier
    x0=bx0
    y0=by0
    cx=3*(bx1-x0)
    bx=3*(bx2-bx1)-cx
    ax=bx3-x0-cx-bx
    cy=3*(by1-y0)
    by=3*(by2-by1)-cy
    ay=by3-y0-cy-by

    return ax,ay,bx,by,cx,cy,x0,y0
    #ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))

def linebezierintersect(arg_a, arg_b):
    ((lx1,ly1),(lx2,ly2)) = arg_a
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = arg_b
    #parametric line
    dd=lx1
    cc=lx2-lx1
    bb=ly1
    aa=ly2-ly1

    if aa:
        coef1=cc/aa
        coef2=1
    else:
        coef1=1
        coef2=aa/cc

    ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))
    #cubic intersection coefficients
    a=coef1*ay-coef2*ax
    b=coef1*by-coef2*bx
    c=coef1*cy-coef2*cx
    d=coef1*(y0-bb)-coef2*(x0-dd)

    roots = rootWrapper(a,b,c,d)
    retval = []
    for i in roots:
        if type(i) is complex and i.imag==0:
            i = i.real
        if type(i) is not complex and 0<=i<=1:
            retval.append(bezierpointatt(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)),i))
    return retval

def bezierpointatt(arg, t):
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = arg
    ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))
    x=ax*(t**3)+bx*(t**2)+cx*t+x0
    y=ay*(t**3)+by*(t**2)+cy*t+y0
    return x,y

def bezierslopeatt(arg, t):
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = arg
    ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))
    dx=3*ax*(t**2)+2*bx*t+cx
    dy=3*ay*(t**2)+2*by*t+cy
    return dx,dy

def beziertatslope(arg, d):
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = arg
    (dy,dx) = d
    ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))
    #quadratic coefficients of slope formula
    if dx:
        slope = 1.0*(dy/dx)
        a=3*ay-3*ax*slope
        b=2*by-2*bx*slope
        c=cy-cx*slope
    elif dy:
        slope = 1.0*(dx/dy)
        a=3*ax-3*ay*slope
        b=2*bx-2*by*slope
        c=cx-cy*slope
    else:
        return []

    roots = rootWrapper(0,a,b,c)
    retval = []
    for i in roots:
        if type(i) is complex and i.imag==0:
            i = i.real
        if type(i) is not complex and 0<=i<=1:
            retval.append(i)
    return retval

def beziersplitatt(arg, t):
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = arg
    m1=tpoint((bx0,by0),(bx1,by1),t)
    m2=tpoint((bx1,by1),(bx2,by2),t)
    m3=tpoint((bx2,by2),(bx3,by3),t)
    m4=tpoint(m1,m2,t)
    m5=tpoint(m2,m3,t)
    m=tpoint(m4,m5,t)

    return ((bx0,by0),m1,m4,m),(m,m5,m3,(bx3,by3))

def numlengths(csplen):
    retval = 0
    for sp in csplen:
        for l in sp:
            if l > 0:
                retval += 1
    return retval

def rootWrapper(a, b, c, d):
    if a:
        # Monics formula see http://en.wikipedia.org/wiki/Cubic_function#Monic_formula_of_roots
        a,b,c = (b/a, c/a, d/a)
        m = 2.0*a**3 - 9.0*a*b + 27.0*c
        k = a**2 - 3.0*b
        n = m**2 - 4.0*k**3
        w1 = -.5 + .5*cmath.sqrt(-3.0)
        w2 = -.5 - .5*cmath.sqrt(-3.0)
        if n < 0:
            m1 = pow(complex((m+cmath.sqrt(n))/2),1./3)
            n1 = pow(complex((m-cmath.sqrt(n))/2),1./3)
        else:
            if m+math.sqrt(n) < 0:
                m1 = -pow(-(m+math.sqrt(n))/2,1./3)
            else:
                m1 = pow((m+math.sqrt(n))/2,1./3)
            if m-math.sqrt(n) < 0:
                n1 = -pow(-(m-math.sqrt(n))/2,1./3)
            else:
                n1 = pow((m-math.sqrt(n))/2,1./3)
        x1 = -1./3 * (a + m1 + n1)
        x2 = -1./3 * (a + w1*m1 + w2*n1)
        x3 = -1./3 * (a + w2*m1 + w1*n1)
        return (x1,x2,x3)
    elif b:
        det=c**2.0-4.0*b*d
        if det:
            return (-c+cmath.sqrt(det))/(2.0*b),(-c-cmath.sqrt(det))/(2.0*b)
        else:
            return -c/(2.0*b),
    elif c:
        return 1.0*(-d/c),
    return ()

def get_fit(u, csp, col):
    return (1-u)**3*csp[0][col] + 3*(1-u)**2*u*csp[1][col] + 3*(1-u)*u**2*csp[2][col] + u**3*csp[3][col]

def get_matrix(u, i, j): 
    if j == i + 2:
        return (u[i]-u[i-1])*(u[i]-u[i-1])/(u[i+2]-u[i-1])/(u[i+1]-u[i-1])
    elif j == i + 1:
        return ((u[i]-u[i-1])*(u[i+2]-u[i])/(u[i+2]-u[i-1]) + (u[i+1]-u[i])*(u[i]-u[i-2])/(u[i+1]-u[i-2]))/(u[i+1]-u[i-1])
    elif j == i:
        return (u[i+1]-u[i])*(u[i+1]-u[i])/(u[i+1]-u[i-2])/(u[i+1]-u[i-1])
    else:
        return 0
