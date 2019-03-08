# coding=utf-8
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
Bezier calculations
"""

import cmath
import math

import numpy

X, Y = range(2)


def pointdistance(point_a, point_b):
    """The size of the line between two points"""
    return math.sqrt(((point_b[X] - point_a[X]) ** 2) + ((point_b[Y] - point_a[Y]) ** 2))


def between_point(point_a, point_b, time=0.5):
    """Returns the point between point a and point b"""
    return point_a[X] + time * (point_b[X] - point_a[X]), point_a[Y] + time * (point_b[Y] - point_a[Y])


def percent_point(point_a, point_b, percent=50.0):
    """Returns between_point but takes percent instead of 0.0-1.0"""
    return between_point(point_a, point_b, percent / 100.0)


def rootWrapper(a, b, c, d):
    if a:
        # Monics formula see http://en.wikipedia.org/wiki/Cubic_function#Monic_formula_of_roots
        a, b, c = (b / a, c / a, d / a)
        m = 2.0 * a ** 3 - 9.0 * a * b + 27.0 * c
        k = a ** 2 - 3.0 * b
        n = m ** 2 - 4.0 * k ** 3
        w1 = -.5 + .5 * cmath.sqrt(-3.0)
        w2 = -.5 - .5 * cmath.sqrt(-3.0)
        if n < 0:
            m1 = pow(complex((m + cmath.sqrt(n)) / 2), 1. / 3)
            n1 = pow(complex((m - cmath.sqrt(n)) / 2), 1. / 3)
        else:
            if m + math.sqrt(n) < 0:
                m1 = -pow(-(m + math.sqrt(n)) / 2, 1. / 3)
            else:
                m1 = pow((m + math.sqrt(n)) / 2, 1. / 3)
            if m - math.sqrt(n) < 0:
                n1 = -pow(-(m - math.sqrt(n)) / 2, 1. / 3)
            else:
                n1 = pow((m - math.sqrt(n)) / 2, 1. / 3)
        x1 = -1. / 3 * (a + m1 + n1)
        x2 = -1. / 3 * (a + w1 * m1 + w2 * n1)
        x3 = -1. / 3 * (a + w2 * m1 + w1 * n1)
        return x1, x2, x3
    elif b:
        det = c ** 2.0 - 4.0 * b * d
        if det:
            return (-c + cmath.sqrt(det)) / (2.0 * b), (-c - cmath.sqrt(det)) / (2.0 * b)
        else:
            return -c / (2.0 * b),
    elif c:
        return 1.0 * (-d / c),
    return ()


def bezlenapprx(sp1, sp2):
    return pointdistance(sp1[1], sp1[2]) \
           + pointdistance(sp1[2], sp2[0]) \
           + pointdistance(sp2[0], sp2[1])


def cspbezsplit(sp1, sp2, time=0.5):
    m1 = tpoint(sp1[1], sp1[2], time)
    m2 = tpoint(sp1[2], sp2[0], time)
    m3 = tpoint(sp2[0], sp2[1], time)
    m4 = tpoint(m1, m2, time)
    m5 = tpoint(m2, m3, time)
    m = tpoint(m4, m5, time)
    return [[sp1[0][:], sp1[1][:], m1], [m4, m, m5], [m3, sp2[1][:], sp2[2][:]]]


def cspbezsplitatlength(sp1, sp2, l=0.5, tolerance=0.001):
    bez = (sp1[1][:], sp1[2][:], sp2[0][:], sp2[1][:])
    time = beziertatlength(bez, l, tolerance)
    return cspbezsplit(sp1, sp2, time)


def cspseglength(sp1, sp2, tolerance=0.001):
    bez = (sp1[1][:], sp1[2][:], sp2[0][:], sp2[1][:])
    return bezierlength(bez, tolerance)


def csplength(csp):
    total = 0
    lengths = []
    for sp in csp:
        lengths.append([])
        for i in range(1, len(sp)):
            l = cspseglength(sp[i - 1], sp[i])
            lengths[-1].append(l)
            total += l
    return lengths, total


def bezierparameterize(arg):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    # parametric bezier
    x0 = bx0
    y0 = by0
    cx = 3 * (bx1 - x0)
    bx = 3 * (bx2 - bx1) - cx
    ax = bx3 - x0 - cx - bx
    cy = 3 * (by1 - y0)
    by = 3 * (by2 - by1) - cy
    ay = by3 - y0 - cy - by

    return ax, ay, bx, by, cx, cy, x0, y0
    # ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))


def linebezierintersect(arg_a, arg_b):
    ((lx1, ly1), (lx2, ly2)) = arg_a
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg_b
    # parametric line
    dd = lx1
    cc = lx2 - lx1
    bb = ly1
    aa = ly2 - ly1

    if aa:
        coef1 = cc / aa
        coef2 = 1
    else:
        coef1 = 1
        coef2 = aa / cc

    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    # cubic intersection coefficients
    a = coef1 * ay - coef2 * ax
    b = coef1 * by - coef2 * bx
    c = coef1 * cy - coef2 * cx
    d = coef1 * (y0 - bb) - coef2 * (x0 - dd)

    roots = rootWrapper(a, b, c, d)
    retval = []
    for i in roots:
        if type(i) is complex and i.imag == 0:
            i = i.real
        if type(i) is not complex and 0 <= i <= 1:
            retval.append(bezierpointatt(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)), i))
    return retval


def bezierpointatt(arg, t):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    x = ax * (t ** 3) + bx * (t ** 2) + cx * t + x0
    y = ay * (t ** 3) + by * (t ** 2) + cy * t + y0
    return x, y


def bezierslopeatt(arg, t):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    dx = 3 * ax * (t ** 2) + 2 * bx * t + cx
    dy = 3 * ay * (t ** 2) + 2 * by * t + cy
    return dx, dy


def beziertatslope(arg, d):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    (dy, dx) = d
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    # quadratic coefficients of slope formula
    if dx:
        slope = 1.0 * (dy / dx)
        a = 3 * ay - 3 * ax * slope
        b = 2 * by - 2 * bx * slope
        c = cy - cx * slope
    elif dy:
        slope = 1.0 * (dx / dy)
        a = 3 * ax - 3 * ay * slope
        b = 2 * bx - 2 * by * slope
        c = cx - cy * slope
    else:
        return []

    roots = rootWrapper(0, a, b, c)
    retval = []
    for i in roots:
        if type(i) is complex and i.imag == 0:
            i = i.real
        if type(i) is not complex and 0 <= i <= 1:
            retval.append(i)
    return retval


def tpoint(p1, p2, t):
    """Linearly interpolate between p1 and p2.

    t = 0.0 returns p1, t = 1.0 returns p2.

    :return: Interpolated point
    :rtype: tuple

    :param p1: First point as sequence of two floats
    :param p2: Second point as sequence of two floats
    :param t: Number between 0.0 and 1.0
    :type t: float
    """
    x1, y1 = p1
    x2, y2 = p2
    return x1 + t * (x2 - x1), y1 + t * (y2 - y1)


def beziersplitatt(arg, t):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    m1 = tpoint((bx0, by0), (bx1, by1), t)
    m2 = tpoint((bx1, by1), (bx2, by2), t)
    m3 = tpoint((bx2, by2), (bx3, by3), t)
    m4 = tpoint(m1, m2, t)
    m5 = tpoint(m2, m3, t)
    m = tpoint(m4, m5, t)

    return ((bx0, by0), m1, m4, m), (m, m5, m3, (bx3, by3))


'''
Approximating the arc length of a bezier curve
according to <http://www.cit.gu.edu.au/~anthony/info/graphics/bezier.curves>

if:
    L1 = |P0 P1| +|P1 P2| +|P2 P3| 
    L0 = |P0 P3|
then: 
    L = 1/2*L0 + 1/2*L1
    ERR = L1-L0
ERR approaches 0 as the number of subdivisions (m) increases
    2^-4m

Reference:
Jens Gravesen <gravesen@mat.dth.dk>
"Adaptive subdivision and the length of Bezier curves"
mat-report no. 1992-10, Mathematical Institute, The Technical
University of Denmark. 
'''


def Gravesen_addifclose(b, len, error=0.001):
    box = 0
    for i in range(1, 4):
        box += pointdistance(b[i - 1], b[i])
    chord = pointdistance(b[0], b[3])
    if (box - chord) > error:
        first, second = beziersplitatt(b, 0.5)
        Gravesen_addifclose(first, len, error)
        Gravesen_addifclose(second, len, error)
    else:
        len[0] += (box / 2.0) + (chord / 2.0)


def bezierlengthGravesen(b, error=0.001):
    len = [0]
    Gravesen_addifclose(b, len, error)
    return len[0]


# balf = Bezier Arc Length Function
balfax, balfbx, balfcx, balfay, balfby, balfcy = 0, 0, 0, 0, 0, 0


def balf(t):
    retval = (balfax * (t ** 2) + balfbx * t + balfcx) ** 2 + (balfay * (t ** 2) + balfby * t + balfcy) ** 2
    return math.sqrt(retval)


def Simpson(f, a, b, n_limit, tolerance):
    n = 2
    multiplier = (b - a) / 6.0
    endsum = f(a) + f(b)
    interval = (b - a) / 2.0
    asum = 0.0
    bsum = f(a + interval)
    est1 = multiplier * (endsum + (2.0 * asum) + (4.0 * bsum))
    est0 = 2.0 * est1
    # print(multiplier, endsum, interval, asum, bsum, est1, est0)
    while n < n_limit and abs(est1 - est0) > tolerance:
        n *= 2
        multiplier /= 2.0
        interval /= 2.0
        asum += bsum
        bsum = 0.0
        est0 = est1
        for i in range(1, n, 2):
            bsum += f(a + (i * interval))
            est1 = multiplier * (endsum + (2.0 * asum) + (4.0 * bsum))
    # print(multiplier, endsum, interval, asum, bsum, est1, est0)
    return est1


def bezierlengthSimpson(arg, tolerance=0.001):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    global balfax, balfbx, balfcx, balfay, balfby, balfcy
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    balfax, balfbx, balfcx, balfay, balfby, balfcy = 3 * ax, 2 * bx, cx, 3 * ay, 2 * by, cy
    return Simpson(balf, 0.0, 1.0, 4096, tolerance)


def beziertatlength(arg, l=0.5, tolerance=0.001):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    global balfax, balfbx, balfcx, balfay, balfby, balfcy
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    balfax, balfbx, balfcx, balfay, balfby, balfcy = 3 * ax, 2 * bx, cx, 3 * ay, 2 * by, cy
    t = 1.0
    tdiv = t
    curlen = Simpson(balf, 0.0, t, 4096, tolerance)
    targetlen = l * curlen
    diff = curlen - targetlen
    while abs(diff) > tolerance:
        tdiv /= 2.0
        if diff < 0:
            t += tdiv
        else:
            t -= tdiv
        curlen = Simpson(balf, 0.0, t, 4096, tolerance)
        diff = curlen - targetlen
    return t


def maxdist(arg):
    ((p0x, p0y), (p1x, p1y), (p2x, p2y), (p3x, p3y)) = arg
    p0 = Point(p0x, p0y)
    p1 = Point(p1x, p1y)
    p2 = Point(p2x, p2y)
    p3 = Point(p3x, p3y)
    s1 = Segment(p0, p3)
    return max(s1.distanceToPoint(p1), s1.distanceToPoint(p2))


def cspsubdiv(csp, flat):
    for sp in csp:
        subdiv(sp, flat)


def subdiv(sp, flat, i=1):
    while i < len(sp):
        p0 = sp[i - 1][1]
        p1 = sp[i - 1][2]
        p2 = sp[i][0]
        p3 = sp[i][1]

        b = (p0, p1, p2, p3)
        m = maxdist(b)
        if m <= flat:
            i += 1
        else:
            one, two = beziersplitatt(b, 0.5)
            sp[i - 1][2] = one[1]
            sp[i][0] = two[2]
            p = [one[2], one[3], two[1]]
            sp[i:1] = [p]


# default bezier length method
bezierlength = bezierlengthSimpson


def csparea(csp):
    area = 0.0
    for sp in csp:
        if len(sp) < 2:
            continue
        for i in range(len(sp)):  # calculate polygon area
            area += 0.5 * sp[i - 1][1][0] * (sp[i][1][1] - sp[i - 2][1][1])
        for i in range(1, len(sp)):  # add contribution from cubic Bezier
            vec_x = numpy.matrix([sp[i - 1][1][0], sp[i - 1][2][0], sp[i][0][0], sp[i][1][0]])
            vec_y = numpy.matrix([sp[i - 1][1][1], sp[i - 1][2][1], sp[i][0][1], sp[i][1][1]])
            area += 0.15 * (vec_x * mat_area * vec_y.T)[0, 0]
    return -area


def cspcofm(csp):
    area = csparea(csp)
    xc = 0.0
    yc = 0.0
    if abs(area) < 1.e-8:
        inkex.errormsg(_("Area is zero, cannot calculate Center of Mass"))
        return 0, 0
    for sp in csp:
        for i in range(len(sp)):  # calculate polygon moment
            xc += sp[i - 1][1][1] * (sp[i - 2][1][0] - sp[i][1][0]) * (sp[i - 2][1][0] + sp[i - 1][1][0] + sp[i][1][0]) / 6
            yc += sp[i - 1][1][0] * (sp[i][1][1] - sp[i - 2][1][1]) * (sp[i - 2][1][1] + sp[i - 1][1][1] + sp[i][1][1]) / 6
        for i in range(1, len(sp)):  # add contribution from cubic Bezier
            vec_x = numpy.matrix([sp[i - 1][1][0], sp[i - 1][2][0], sp[i][0][0], sp[i][1][0]])
            vec_y = numpy.matrix([sp[i - 1][1][1], sp[i - 1][2][1], sp[i][0][1], sp[i][1][1]])
            vec_t = numpy.matrix([(vec_x * mat_cofm_0 * vec_y.T)[0, 0], (vec_x * mat_cofm_1 * vec_y.T)[0, 0], (vec_x * mat_cofm_2 * vec_y.T)[0, 0], (vec_x * mat_cofm_3 * vec_y.T)[0, 0]])
            xc += (vec_x * vec_t.T)[0, 0] / 280
            yc += (vec_y * vec_t.T)[0, 0] / 280
    return -xc / area, -yc / area


def bezierparameterize(arg):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    # parametric bezier
    x0 = bx0
    y0 = by0
    cx = 3 * (bx1 - x0)
    bx = 3 * (bx2 - bx1) - cx
    ax = bx3 - x0 - cx - bx
    cy = 3 * (by1 - y0)
    by = 3 * (by2 - by1) - cy
    ay = by3 - y0 - cy - by

    return ax, ay, bx, by, cx, cy, x0, y0
    # ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))


def linebezierintersect(arg_a, arg_b):
    ((lx1, ly1), (lx2, ly2)) = arg_a
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg_b
    # parametric line
    dd = lx1
    cc = lx2 - lx1
    bb = ly1
    aa = ly2 - ly1

    if aa:
        coef1 = cc / aa
        coef2 = 1
    else:
        coef1 = 1
        coef2 = aa / cc

    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    # cubic intersection coefficients
    a = coef1 * ay - coef2 * ax
    b = coef1 * by - coef2 * bx
    c = coef1 * cy - coef2 * cx
    d = coef1 * (y0 - bb) - coef2 * (x0 - dd)

    roots = rootWrapper(a, b, c, d)
    retval = []
    for i in roots:
        if type(i) is complex and i.imag == 0:
            i = i.real
        if type(i) is not complex and 0 <= i <= 1:
            retval.append(bezierpointatt(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)), i))
    return retval


def bezierpointatt(arg, t):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    x = ax * (t ** 3) + bx * (t ** 2) + cx * t + x0
    y = ay * (t ** 3) + by * (t ** 2) + cy * t + y0
    return x, y


def bezierslopeatt(arg, t):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    dx = 3 * ax * (t ** 2) + 2 * bx * t + cx
    dy = 3 * ay * (t ** 2) + 2 * by * t + cy
    return dx, dy


def beziertatslope(arg, d):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    (dy, dx) = d
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    # quadratic coefficients of slope formula
    if dx:
        slope = 1.0 * (dy / dx)
        a = 3 * ay - 3 * ax * slope
        b = 2 * by - 2 * bx * slope
        c = cy - cx * slope
    elif dy:
        slope = 1.0 * (dx / dy)
        a = 3 * ax - 3 * ay * slope
        b = 2 * bx - 2 * by * slope
        c = cx - cy * slope
    else:
        return []

    roots = rootWrapper(0, a, b, c)
    retval = []
    for i in roots:
        if type(i) is complex and i.imag == 0:
            i = i.real
        if type(i) is not complex and 0 <= i <= 1:
            retval.append(i)
    return retval


def beziersplitatt(arg, t):
    ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)) = arg
    m1 = tpoint((bx0, by0), (bx1, by1), t)
    m2 = tpoint((bx1, by1), (bx2, by2), t)
    m3 = tpoint((bx2, by2), (bx3, by3), t)
    m4 = tpoint(m1, m2, t)
    m5 = tpoint(m2, m3, t)
    m = tpoint(m4, m5, t)

    return ((bx0, by0), m1, m4, m), (m, m5, m3, (bx3, by3))


def numlengths(csplen):
    retval = 0
    for sp in csplen:
        for l in sp:
            if l > 0:
                retval += 1
    return retval


if __name__ == '__main__':
    # print(linebezierintersect(((,),(,)),((,),(,),(,),(,))))
    # print(linebezierintersect(((0,1),(0,-1)),((-1,0),(-.5,0),(.5,0),(1,0))))
    tol = 0.00000001
    curves = [((0, 0), (1, 5), (4, 5), (5, 5)),
              ((0, 0), (0, 0), (5, 0), (10, 0)),
              ((0, 0), (0, 0), (5, 1), (10, 0)),
              ((-10, 0), (0, 0), (10, 0), (10, 10)),
              ((15, 10), (0, 0), (10, 0), (-5, 10))]
    '''
    for curve in curves:
        timing.start()
        g = bezierlengthGravesen(curve,tol)
        timing.finish()
        gt = timing.micro()

        timing.start()
        s = bezierlengthSimpson(curve,tol)
        timing.finish()
        st = timing.micro()

        print g, gt
        print s, st
    '''
    for curve in curves:
        print(beziertatlength(curve, 0.5))
